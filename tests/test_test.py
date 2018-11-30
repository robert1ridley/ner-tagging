from utils import load_file, get_test_data_sets, get_emission_probabilities, get_transition_probabilities
from models import viterbi


def main():
  TEST_FILE = '../data/test.content.txt'
  EMISSION_PROBABILITIES = '../data/emission_probabilities.txt'
  TRANSITION_PROBABILITIES = '../data/transition_probabilities.txt'

  emission_probabilities = get_emission_probabilities(EMISSION_PROBABILITIES)
  transition_probabilities = get_transition_probabilities(TRANSITION_PROBABILITIES)

  pred_sets = []
  test_data = load_file(TEST_FILE)
  test_data_sets = get_test_data_sets(test_data)
  for set in test_data_sets:
    pred = viterbi(set, transition_probabilities, emission_probabilities)
    pred_sets.append(pred)

  pred_string = ''
  for predict in pred_sets:
    joined_string = ' '.join(predict)
    pred_string += joined_string + '\n'


  with open('../data/prediction_finalv2.txt', "w") as f:
    f.write(pred_string)


if __name__ == '__main__':
    main()