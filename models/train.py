import torch
from utils import calc_arg_max, compute_log_sum_expectation, prepare_sequence, \
  load_vocabulary_and_tags, generate_tag_dictionary, generate_vocab_dictionary, get_training_data, load_file

START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
EMBEDDING_DIM = 5
HIDDEN_DIM = 4

class BiLSTM(torch.nn.Module):

  def __init__(self, vocab_size, tag_to_ix, embedding_dim, hidden_dim):
    super(BiLSTM, self).__init__()
    self.embedding_dim = embedding_dim
    self.hidden_dim = hidden_dim
    self.vocab_size = vocab_size
    self.tag_to_ix = tag_to_ix
    self.tagset_size = len(tag_to_ix)

    self.word_embeds = torch.nn.Embedding(vocab_size, embedding_dim)
    self.lstm = torch.nn.LSTM(embedding_dim, hidden_dim // 2,
                        num_layers=1, bidirectional=True)
    self.hidden2tag = torch.nn.Linear(hidden_dim, self.tagset_size)
    self.transitions = torch.nn.Parameter(
      torch.randn(self.tagset_size, self.tagset_size))
    self.transitions.data[tag_to_ix[START_SYMBOL], :] = -10000
    self.transitions.data[:, tag_to_ix[STOP_SYMBOL]] = -10000

    self.hidden = self.init_hidden()

  def init_hidden(self):
    return (torch.randn(2, 1, self.hidden_dim // 2),
            torch.randn(2, 1, self.hidden_dim // 2))


  def _forward_alg(self, feats):
    init_alphas = torch.full((1, self.tagset_size), -10000.)
    init_alphas[0][self.tag_to_ix[START_SYMBOL]] = 0.
    forward_var = init_alphas

    for feat in feats:
      alphas_t = []
      for next_tag in range(self.tagset_size):
        emit_score = feat[next_tag].view(
          1, -1).expand(1, self.tagset_size)
        trans_score = self.transitions[next_tag].view(1, -1)
        next_tag_var = forward_var + trans_score + emit_score
        alphas_t.append(compute_log_sum_expectation(next_tag_var).view(1))
      forward_var = torch.cat(alphas_t).view(1, -1)
    terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_SYMBOL]]
    alpha = compute_log_sum_expectation(terminal_var)
    return alpha


  def _get_lstm_features(self, sentence):
    self.hidden = self.init_hidden()
    embeds = self.word_embeds(sentence).view(len(sentence), 1, -1)
    lstm_out, self.hidden = self.lstm(embeds, self.hidden)
    lstm_out = lstm_out.view(len(sentence), self.hidden_dim)
    lstm_feats = self.hidden2tag(lstm_out)
    return lstm_feats


  def _score_sentence(self, feats, tags):
    score = torch.zeros(1)
    tags = torch.cat([torch.tensor([self.tag_to_ix[START_SYMBOL]], dtype=torch.long), tags])
    for i, feat in enumerate(feats):
      score = score + \
              self.transitions[tags[i + 1], tags[i]] + feat[tags[i + 1]]
    score = score + self.transitions[self.tag_to_ix[STOP_SYMBOL], tags[-1]]
    return score


  def _viterbi_decode(self, feats):
    backpointers = []

    init_vvars = torch.full((1, self.tagset_size), -10000.)
    init_vvars[0][self.tag_to_ix[START_SYMBOL]] = 0

    forward_var = init_vvars
    for feat in feats:
      bptrs_t = []
      viterbivars_t = []

      for next_tag in range(self.tagset_size):
        next_tag_var = forward_var + self.transitions[next_tag]
        best_tag_id = calc_arg_max(next_tag_var)
        bptrs_t.append(best_tag_id)
        viterbivars_t.append(next_tag_var[0][best_tag_id].view(1))
      forward_var = (torch.cat(viterbivars_t) + feat).view(1, -1)
      backpointers.append(bptrs_t)

    terminal_var = forward_var + self.transitions[self.tag_to_ix[STOP_SYMBOL]]
    best_tag_id = calc_arg_max(terminal_var)
    path_score = terminal_var[0][best_tag_id]
    best_path = [best_tag_id]
    for bptrs_t in reversed(backpointers):
      best_tag_id = bptrs_t[best_tag_id]
      best_path.append(best_tag_id)
    start = best_path.pop()
    assert start == self.tag_to_ix[START_SYMBOL]
    best_path.reverse()
    return path_score, best_path


  def neg_log_likelihood(self, sentence, tags):
    feats = self._get_lstm_features(sentence)
    forward_score = self._forward_alg(feats)
    gold_score = self._score_sentence(feats, tags)
    return forward_score - gold_score


  def forward(self, sentence):
    lstm_feats = self._get_lstm_features(sentence)
    score, tag_seq = self._viterbi_decode(lstm_feats)
    return score, tag_seq


def main():
  word_list, tag_list = load_vocabulary_and_tags('../data/')
  word_dict = generate_vocab_dictionary(word_list)
  tag_dict = generate_tag_dictionary(tag_list)
  model = BiLSTM(len(word_list), tag_dict, EMBEDDING_DIM, HIDDEN_DIM)
  optimizer = torch.optim.SGD(model.parameters(), lr=0.01, weight_decay=1e-4)
  data = load_file('../data/dev.txt')
  training_data = get_training_data(data)
  training_data = training_data[:10]
  with torch.no_grad():
    precheck_sent = prepare_sequence(training_data[5][0], word_dict)
    precheck_tags = torch.tensor([tag_dict[t] for t in training_data[0][1]], dtype=torch.long)
    print(model(precheck_sent))

  for epoch in range(
    50):
    print(epoch)
    for sentence, tags in training_data:
      model.zero_grad()
      sentence_in = prepare_sequence(sentence, word_dict)
      targets = torch.tensor([tag_dict[t] for t in tags], dtype=torch.long)
      loss = model.neg_log_likelihood(sentence_in, targets)
      loss.backward()
      optimizer.step()

  with torch.no_grad():
    precheck_sent = prepare_sequence(training_data[5][0], word_dict)
    print(model(precheck_sent))


if __name__ == "__main__":
  main()
