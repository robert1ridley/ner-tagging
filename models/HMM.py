from utils import get_pairs, load_file
from nltk import bigrams, trigrams
from collections import defaultdict
import math


def is_in_emissions_dict(word, emissions_dict):
  for k, v in emissions_dict.items():
    if word in v.keys():
      return True
  return False


def viterbi(states, sentence, transition, emission):
  sentence.insert(0, '*')
  sentence.insert(0, '*')
  sentence.append('STOP')
  paths = [[]]

  # Calc initial paths
  index = 2
  initial_word = sentence[index]
  word_in_dict = is_in_emissions_dict(initial_word, emission)
  if not word_in_dict:
    initial_word = '_RARE_'
  for item in transition:
    if item[0] == '*' and item[1] == '*':
      current_tag = item[2]
      if current_tag in emission.keys():
        if initial_word in emission[current_tag].keys():
          probability = float(emission[current_tag][initial_word]) * float(transition[item])
          paths[0].append((item, probability))
  index += 1

  # Calc remaining paths
  while index < len(sentence):
    current_word = sentence[index]
    prev_instances = paths[-1]
    paths.append([])
    for item in prev_instances:
      tag1 = item[0][1]
      tag2 = item[0][2]
      word_in_dict = is_in_emissions_dict(current_word, emission)
      if not word_in_dict:
        current_word = '_RARE_'
      for tran in transition:
        if tran[0] == tag1 and tran[1] == tag2:
          current_tag = tran[2]
          if current_tag in emission.keys():
            if current_word in emission[current_tag].keys():
              probability = float(emission[current_tag][current_word]) * float(transition[tran])
              if (tran, probability) not in paths[-1]:
                paths[-1].append((tran, probability))
    index += 1
  rev = paths[::-1]
  for path in rev:
    print(path)

  # Backpointers calc
  path_options = []
  final_index = len(paths) - 1
  for result in paths[final_index]:
    path_options.append([(result[0][2], result[1])])
    prev = result[0][1]
    skip_prev = result[0][0]
    current_index = final_index - 1
    while current_index >= -1:
      for item in paths[current_index]:
        if item[0][1] == skip_prev and item[0][2] == prev:
          path_options[-1].append((item[0][2], item[1]))
          prev = item[0][1]
          skip_prev = item[0][0]
        current_index -= 1
    final_index -= 1
  # print(path_options)



def calculate_emissions(sentences):
  emission_count = {}
  term = 'ONEGRAM '
  for sentence in sentences:
    for pair in sentence:
      if term + pair[0] + ' ' + pair[1] not in emission_count.keys():
        emission_count[term + pair[0] + ' ' + pair[1]] = 1
      else:
        emission_count[term + pair[0] + ' ' + pair[1]] += 1

  new_dict = emission_count.copy()
  for emission in emission_count.keys():
    split = emission.strip().split()
    term = split[0]
    word = split[1]
    tag = split[2]
    if new_dict[emission] < 5:
      if term + ' ' + '_RARE_' + ' ' + tag not in new_dict.keys():
        new_dict[term + ' ' + '_RARE_' + ' ' + tag] = new_dict[emission]
      else:
        new_dict[term + ' ' + '_RARE_' + ' ' + tag] += new_dict[emission]
  final_dict = {}
  for k, v in new_dict.items():
    if not v < 5:
      final_dict[k] = v
  return final_dict


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


def get_states(pathname):
  states = load_file(pathname)
  state_list = []
  for state in states:
    state_list.append(state.strip())
  return state_list


def get_observations(pathname):
  observations = load_file(pathname)
  observation_list = []
  for observation in observations:
    observation = observation.strip().split()
    gram = observation[0]
    word = observation[1]
    if gram == 'ONEGRAM' and word not in observation_list:
      observation_list.append(word)
  return observation_list


def get_initial_probs(pathname):
  emissions = load_file(pathname)
  counts = {}
  probs = {}
  for emission in emissions:
    split = emission.strip().split()
    if split[0] == 'TRIGRAM' and split[1] == '*' and split[2] == '*':
      counts[split[3]] = int(split[4])
  total = sum(counts.values())
  for item in counts:
    probs[item] = counts[item]/total
  return probs


def get_emission_probabilities(pathname):
  emission_probs = load_file(pathname)
  emission_probs_dict = {}
  for emission in emission_probs:
    emission = emission.strip().split()
    word = emission[0]
    tag = emission[1]
    probability = emission[2]
    if tag not in emission_probs_dict.keys():
      inner_dict = {}
      inner_dict[word] = probability
      emission_probs_dict[tag] = inner_dict
    else:
      emission_probs_dict[tag][word] = probability
  return emission_probs_dict


def get_transition_probabilities(pathname):
  transition_probs = load_file(pathname)
  transition_probs_dict = {}
  for transition in transition_probs:
    inter = transition.strip().split('|')
    final_state = inter[0].strip()
    bigram_and_prob = inter[1].split()
    key = (bigram_and_prob[0], bigram_and_prob[1], final_state)
    transition_probs_dict[key] = bigram_and_prob[2]
  return transition_probs_dict


def get_words(pathname):
  file_data = load_file(pathname)
  d = defaultdict(int)
  for l in file_data:
    line = l.strip().split()
    if line[0] == 'ONEGRAM':
      word = line[1]
      d[word] = line[3]
  return d


def main():
  EMISSION_COUNT_FILE = '../data/emission_counts.txt'
  EMISSION_PROBABILITIES = '../data/emission_probabilities.txt'
  TRANSITION_PROBABILITIES = '../data/transition_probabilities.txt'
  TRAINING_FILE = '../data/train.txt'
  TAG_COUNTS = '../data/tag_counts.txt'
  TAGS = '../data/tags.txt'

  # calculate_and_write_emmision_counts(TRAINING_FILE, EMISSION_COUNT_FILE, TAG_COUNTS)
  # start_count_emission_probabilities(EMISSION_COUNT_FILE, TAG_COUNTS, EMISSION_PROBABILITIES)
  # start_count_transition_probabilities(EMISSION_COUNT_FILE, TRANSITION_PROBABILITIES)
  # words = get_words(EMISSION_COUNT_FILE)
  states = get_states(TAGS)

  # EMIS = {{'O': '他': '0.0030924176793756647', ...}, {I-ORG: ...}}
  emission_probabilities = get_emission_probabilities(EMISSION_PROBABILITIES)

  # TRANS = {('*', '*', '0'): 0.643242, ...}
  transition_probabilities = get_transition_probabilities(TRANSITION_PROBABILITIES)
  obs = ['习近平', '是', '我的', '朋友']
  viterbi(states, obs, transition_probabilities, emission_probabilities)


if __name__ == '__main__':
  main()
