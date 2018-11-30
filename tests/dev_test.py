from sklearn.metrics import f1_score
from sklearn.preprocessing import MultiLabelBinarizer
from utils import load_file, get_emission_probabilities, \
  get_transition_probabilities, get_dev_words_and_tags
from models import viterbi


def main():
  EMISSION_PROBABILITIES = '../data/emission_probabilities.txt'
  TRANSITION_PROBABILITIES = '../data/transition_probabilities.txt'
  DEV_FILE = '../data/dev.txt'

  emission_probabilities = get_emission_probabilities(EMISSION_PROBABILITIES)
  transition_probabilities = get_transition_probabilities(TRANSITION_PROBABILITIES)

  tags_sets = []
  dev_data = load_file(DEV_FILE)
  word_obs, dev_tags = get_dev_words_and_tags(dev_data)
  for obs in word_obs:
    predicted_tags = viterbi(obs, transition_probabilities, emission_probabilities)
    tags_sets.append(predicted_tags)

  correct = 0
  incorrect = 0
  set_count = 0
  for set in tags_sets:
    tag_count = 0
    for tag in set:
      if tag == dev_tags[set_count][tag_count]:
        correct += 1
      else:
        incorrect += 1
      tag_count += 1
    set_count += 1
  print("ACCURACY: " + str(correct/(correct+incorrect)))
  new_preds = MultiLabelBinarizer().fit_transform(tags_sets)
  true_tags = MultiLabelBinarizer().fit_transform(dev_tags)
  score = f1_score(true_tags, new_preds, average="micro")
  print("F1-SCORE: " + str(score))

if __name__ == '__main__':
  main()