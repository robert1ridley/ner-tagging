from math import log
import os, sys
import _pickle
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import utils


def compute_emission_probabilities(word_and_tag_count, tag_occurence_count):
  em_probs = {}
  for word_and_tag, count in word_and_tag_count.items():
    # TRY THIS WITHOUT LOG
    em_probs[word_and_tag] = log(float(count)/float(tag_occurence_count[word_and_tag[1]]))
  return em_probs


def compute_transition_probabilities(trigram_occurence_count, bigram_occurence_count, tag_set):
  tran_probs = {}
  for trigram, count in trigram_occurence_count.items():
    bigram_count = bigram_occurence_count[(trigram[0],trigram[1])]
    tag_num = len(tag_set)
    tran_probs[trigram] = log(float(count+1)/float(bigram_count + tag_num))
  return tran_probs


def main():
  TRAINING_DATA = './data/train.txt'
  train_data = utils.load_file(TRAINING_DATA)
  prepare_data = utils.Prepare_data()
  word_tag_pairs = prepare_data.get_pairs(train_data)
  word_tag_appearances = prepare_data.word_tag_appearances
  tag_set = prepare_data.tag_set
  word_and_tag_count = {}
  tag_occurence_count = {}
  bigram_occurence_count = {}
  trigram_occurence_count = {}
  for sentence in word_tag_pairs:
    for i in range(2, len(sentence)):
      if sentence[i] in word_and_tag_count:
        word_and_tag_count[sentence[i]] += 1
      else:
        word_and_tag_count[sentence[i]] = 1

      ner_tag = sentence[i][1]
      if ner_tag in tag_occurence_count:
        tag_occurence_count[ner_tag] += 1
      else:
        tag_occurence_count[ner_tag] = 1

      # TRY SOMETHING LIKE (sentence[i-1][1], sentence[i][1])
      bigrams = (sentence[i-2][1], sentence[i-1][1])
      if bigrams in bigram_occurence_count:
        bigram_occurence_count[bigrams] += 1
      else:
        bigram_occurence_count[bigrams] = 1

      trigrams = (sentence[i-2][1], sentence[i-1][1], sentence[i][1])
      if trigrams in trigram_occurence_count:
        trigram_occurence_count[trigrams] += 1
      else:
        trigram_occurence_count[trigrams] = 1

  emission_probabilities = compute_emission_probabilities(word_and_tag_count, tag_occurence_count)
  transition_probabilities = compute_transition_probabilities(trigram_occurence_count, bigram_occurence_count, tag_set)

  probabilities = {
    'transitions': transition_probabilities,
    'emissions': emission_probabilities,
    'word_tag_appearance': word_tag_appearances,
    'tag_set': tag_set,
    'bigrams': bigram_occurence_count
  }
  with open('./data/probabilities.txt', 'wb') as outfile:
    _pickle.dump(probabilities, outfile)


if __name__ == '__main__':
  main()