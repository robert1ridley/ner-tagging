import torch


def calc_arg_max(vector):
  _, idx = torch.max(vector, 1)
  return idx.item()


def prepare_sequence(sequence, to_idx):
  idxs = [to_idx[w] for w in sequence]
  return torch.tensor(idxs, dtype=torch.long)


def compute_log_sum_expectation(vector):
  max_score = vector[0, calc_arg_max(vector)]
  max_score_broadcast = max_score.view(1, -1).expand(1, vector.size()[1])
  return max_score + torch.log(torch.sum(torch.exp(vector - max_score_broadcast)))