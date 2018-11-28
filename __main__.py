
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000

def split_words_and_tags(training_data):
  training_tags = []
  training_words = []
  for sentence in training_data:
    current_sentence_words = []
    current_sentence_tags = []
    sentence = (START_SYMBOL + "/" + START_SYMBOL + " ") * 2 + sentence + " " + STOP_SYMBOL + "/" + STOP_SYMBOL
    for word in sentence.strip().split():
      splits = word.rsplit('/', 1)
      current_sentence_words.append(splits[0])
      current_sentence_tags.append(splits[1])
    training_words.append(current_sentence_words)
    training_tags.append(current_sentence_tags)
  return training_words, training_tags


def get_words_and_tags(data):
  word_tag_list = []
  for word in data.strip().split():
    splits = word.rsplit('/', 1)
    word_tag_list.append(splits)
  return word_tag_list


def main():
  infile = open('./data/dev.txt', 'r')
  data = infile.read()
  infile.close()

  word_tag_pairs = get_words_and_tags(data)



if __name__ == '__main__':
    main()