import os, sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
import _pickle
from models import Viterbi
from utils import load_file, get_dev_words_and_tags
from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer


class Dev_test(object):

  def __init__(self):
    self.transition_probabilities = {}
    self.emission_probabilities = {}
    self.word_tags_set = {}
    self.unique_tags = {}
    self.bigram_counts = {}
    self.test_data = None
    self.actual_tags = []
    self.predicted_tags = []


  def get_params(self, probs_dict):
    self.transition_probabilities = probs_dict['transitions']
    self.emission_probabilities = probs_dict['emissions']
    self.word_tags_set = probs_dict['word_tag_appearance']
    self.unique_tags = probs_dict['tag_set']
    self.bigram_counts = probs_dict['bigrams']


  def get_data(self, filename):
    dev_data = load_file(filename)
    word_obs, dev_tags = get_dev_words_and_tags(dev_data)
    for sent in dev_tags:
      self.actual_tags.append(sent[2:])
    self.test_data = word_obs


  def run_viterbi(self):
    viterbi = Viterbi(self.transition_probabilities, self.emission_probabilities,
                      self.word_tags_set, self.unique_tags, self.bigram_counts, self.test_data)
    self.predicted_tags = viterbi.calc_viterbi()


  def calc_accuracy(self):
    correct = 0
    incorrect = 0
    set_count = 0
    labels = []
    classes = ('O', 'B-LOCATION', 'B-TIME', 'B-PERSON', 'O-PERSON', 'B-ORGANIZATION',
               'O-ORGANIZATION', 'O-LOCATION', 'I-ORGANIZATION', 'I-LOCATION')
    for set in self.actual_tags:
      tag_count = 0
      for tag in set:
        if tag not in labels:
          labels.append(tag)
        if tag == self.predicted_tags[set_count][tag_count]:
          correct += 1
        else:
          incorrect += 1
        tag_count += 1
      set_count += 1
    print("ACCURACY: " + str(correct / (correct + incorrect)))
    predictions = MultiLabelBinarizer(classes=classes).fit_transform(self.predicted_tags)
    true_tags = MultiLabelBinarizer(classes=classes).fit_transform(self.actual_tags)
    score = f1_score(true_tags, predictions, average="micro")
    print("F1-SCORE: " + str(score))


def main():
  DEV_FILE = './data/dev.txt'
  PROBABILITIES_FILE = './data/probabilities.txt'

  with open(PROBABILITIES_FILE, 'rb') as infile:
    probs_dict = _pickle.load(infile)
  dev_test = Dev_test()
  dev_test.get_params(probs_dict)
  dev_test.get_data(DEV_FILE)
  dev_test.run_viterbi()
  dev_test.calc_accuracy()


if __name__ == '__main__':
    main()