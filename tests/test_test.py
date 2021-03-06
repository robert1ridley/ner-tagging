import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _pickle
from models import Viterbi
from utils import load_file, get_test_data_sets


class Test_test(object):

  def __init__(self):
    self.transition_probabilities = {}
    self.emission_probabilities = {}
    self.word_tags_set = {}
    self.unique_tags = {}
    self.bigram_counts = {}
    self.test_data = None
    self.predicted_tags = []


  def get_params(self, probs_dict):
    self.transition_probabilities = probs_dict['transitions']
    self.emission_probabilities = probs_dict['emissions']
    self.word_tags_set = probs_dict['word_tag_appearance']
    self.unique_tags = probs_dict['tag_set']
    self.bigram_counts = probs_dict['bigrams']


  def get_data(self, filename):
    test_data = load_file(filename)
    word_obs = get_test_data_sets(test_data)
    self.test_data = word_obs


  def run_viterbi(self):
    viterbi = Viterbi(self.transition_probabilities, self.emission_probabilities,
                      self.word_tags_set, self.unique_tags, self.bigram_counts, self.test_data)
    self.predicted_tags = viterbi.calc_viterbi()


  def write_to_file(self, output_file):
    pred_string = ''
    for predict in self.predicted_tags:
      predicted_sequence = ' '.join(predict)
      pred_string += predicted_sequence + '\n'

    with open(output_file, "w") as f:
      f.write(pred_string)


def main():
  TEST_FILE = './data/test.content.txt'
  PROBABILITIES_FILE = './data/probabilities.txt'
  OUTPUT_FILE = './data/predictions.txt'

  with open(PROBABILITIES_FILE, 'rb') as infile:
    probs_dict = _pickle.load(infile)
  test_test = Test_test()
  test_test.get_params(probs_dict)
  test_test.get_data(TEST_FILE)
  test_test.run_viterbi()
  test_test.write_to_file(OUTPUT_FILE)


if __name__ == '__main__':
    main()