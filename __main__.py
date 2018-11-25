
START_SYMBOL = '*'
STOP_SYMBOL = 'STOP'
RARE_SYMBOL = '_RARE_'
RARE_WORD_MAX_FREQ = 5
LOG_PROB_OF_ZERO = -1000

def split_words_and_tags(training_data):
  training_tags = [[wordtag.rsplit('/', 1)[-1] for wordtag in sentence.strip().split()] for sentence in training_data]
  training_tags = [[START_SYMBOL] * 2 + sent_tags + [STOP_SYMBOL] for sent_tags in training_tags]

  training_words = [[wordtag.rsplit('/', 1)[0] for wordtag in sentence.strip().split()] for sentence in training_data]
  training_words = [[START_SYMBOL] * 2 + sent_words + [STOP_SYMBOL] for sent_words in training_tags]
  return training_words, training_tags


def main():
  infile = open('./data/dev.txt', 'r')
  data = infile.readlines()
  infile.close()

  words, tags = split_words_and_tags(data)
  print(words)


if __name__ == '__main__':
    main()