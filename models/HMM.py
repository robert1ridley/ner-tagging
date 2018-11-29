from utils import get_pairs, load_file
from nltk import bigrams, trigrams


class Hmm(object):

  def __init__(self):
    pass


def calculate_emissions(sentences):
  emission_count = {}
  term = 'ONEGRAM '
  for sentence in sentences:
    for pair in sentence:
      if term + pair[0] + ' ' + pair[1] not in emission_count.keys():
        emission_count[term + pair[0] + ' ' + pair[1]] = 1
      else:
        emission_count[term + pair[0] + ' ' + pair[1]] += 1
  return emission_count


def calc_bigram_emissions(sequence_sets):
  bigram_emission_dict = {}
  term = 'BIGRAM '
  for seq in sequence_sets:
    biGr = list(bigrams(seq))
    for item in biGr:
      if term + item[0] + ' ' + item[1] not in bigram_emission_dict.keys():
        bigram_emission_dict[term + item[0] + ' ' + item[1]] = 1
      else:
        bigram_emission_dict[term + item[0] + ' ' + item[1]] += 1
  return bigram_emission_dict


def calc_trigram_emissions(sequence_sets):
  trigram_emission_dict = {}
  term = 'TRIGRAM '
  for seq in sequence_sets:
    trGr = list(trigrams(seq))
    for item in trGr:
      if term + item[0] + ' ' + item[1] + ' ' + item[2] not in trigram_emission_dict.keys():
        trigram_emission_dict[term + item[0] + ' ' + item[1] + ' ' + item[2]] = 1
      else:
        trigram_emission_dict[term + item[0] + ' ' + item[1] + ' ' + item[2]] += 1
  return trigram_emission_dict


def get_tag_seqs(sentences):
  sets = []
  for sentence in sentences:
    tags = []
    for pair in sentence:
      tags.append(pair[1])
    sets.append(tags)
  return sets


def write_emissions_to_text(_words, _bigrams, _trigrams, pathname):
  text = ''
  for key in _words:
    text += key + ' ' + str(_words[key]) + '\n'
  for key in _bigrams:
    text += key + ' ' + str(_bigrams[key]) + '\n'
  for key in _trigrams:
    text += key + ' ' + str(_trigrams[key]) + '\n'
  with open(pathname, "w") as f:
    f.write(text)


def write_tag_counts_to_text(tag_seqs, pathname):
  tags = {}
  tag_string = ''
  for sentence in tag_seqs:
    for tag in sentence:
      if tag not in tags:
        tags[tag] = 1
      else:
        tags[tag] += 1
  for key in tags:
    tag_string += key + ' ' + str(tags[key]) + '\n'
  with open(pathname, "w") as f:
    f.write(tag_string)


def calculate_emission_probabilities(emission_counts, tag_counts):
  emission_count_data = load_file(emission_counts)
  tag_count_data = load_file(tag_counts)
  tag_count_dict = {}
  for tag_set in tag_count_data:
    tag_set = tag_set.strip().split()
    tag_count_dict[tag_set[0]] = int(tag_set[1])

  scores = {}
  for datum in emission_count_data:
    datum = datum.strip().split()
    if datum[0] == 'ONEGRAM':
      term = datum[1]
      tag = datum[2]
      emission_count = int(datum[3])
      score = emission_count / tag_count_dict[tag]
      scores[term + ' ' + tag] = score
  return scores


def write_emission_probabilities_to_text(emission_dict, pathname):
  text = ''
  for key in emission_dict:
    text += key + ' ' + str(emission_dict[key]) + '\n'
  with open(pathname, "w") as f:
    f.write(text)


def calculate_and_write_emmision_counts(TRAINING_FILE, EMISSION_COUNT_FILE, TAG_COUNTS):
  data = load_file(TRAINING_FILE)
  sentences = get_pairs(data)
  tag_seqs = get_tag_seqs(sentences)
  onegram_emissions = calculate_emissions(sentences)
  bigram_emissions = calc_bigram_emissions(tag_seqs)
  trigram_emissions = calc_trigram_emissions(tag_seqs)
  write_emissions_to_text(onegram_emissions, bigram_emissions, trigram_emissions, EMISSION_COUNT_FILE)
  write_tag_counts_to_text(tag_seqs, TAG_COUNTS)


def start_count_emission_probabilities(EMISSION_COUNT_FILE, TAG_COUNTS, EMISSION_PROBABILITIES):
  emission_probabilities = calculate_emission_probabilities(EMISSION_COUNT_FILE, TAG_COUNTS)
  write_emission_probabilities_to_text(emission_probabilities, EMISSION_PROBABILITIES)


def calculate_transition_probabilities(EMISSION_COUNT_FILE):
  emission_count_data = load_file(EMISSION_COUNT_FILE)
  scores = {}
  bigram_dict = {}
  for datum in emission_count_data:
    datum = datum.strip().split()
    if datum[0] == 'BIGRAM':
      bigram_dict[datum[1] + ' ' + datum[2]] = int(datum[3])
    elif datum[0] == 'TRIGRAM':
      tag1 = datum[1]
      tag2 = datum[2]
      tag3 = datum[3]
      trigram_count = int(datum[4])
      score = trigram_count/bigram_dict[tag1 + ' ' + tag2]
      scores[tag3 + ' | ' + tag1 + ' ' + tag2] = score
  return scores


def write_transition_probabilities_to_text(transition_probabilities, pathname):
  text = ''
  for key in transition_probabilities:
    text += key + ' ' + str(transition_probabilities[key]) + '\n'
  with open(pathname, "w") as f:
    f.write(text)


def start_count_transition_probabilities(EMISSION_COUNT_FILE, TRANSITION_PROBABILITIES):
  # SCORES ARE RETURNED IN THE FORM (y | y-2, y-1)
  transition_probabilities = calculate_transition_probabilities(EMISSION_COUNT_FILE)
  write_transition_probabilities_to_text(transition_probabilities, TRANSITION_PROBABILITIES)


def main():
  EMISSION_COUNT_FILE = '../data/emission_counts.txt'
  EMISSION_PROBABILITIES = '../data/emission_probabilities.txt'
  TRANSITION_PROBABILITIES = '../data/transition_probabilities.txt'
  TRAINING_FILE = '../data/train.txt'
  TAG_COUNTS = '../data/tag_counts.txt'


  # start_count_transition_probabilities(EMISSION_COUNT_FILE, TRANSITION_PROBABILITIES)


if __name__ == '__main__':
  main()
