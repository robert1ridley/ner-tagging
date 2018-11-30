from utils import load_file

START_SYMBOL = '*\n'
STOP_SYMBOL = 'STOP\n'


def get_test_data_sets(data):
  sets = []
  for line in data:
    set = line.strip().split()
    sets.append(set)
  return sets


def get_dev_words_and_tags(data):
  words = []
  tags = []
  for sentence in data:
    sentence_words = []
    sentence_tags = []
    for word in sentence.strip().split():
      splits = word.rsplit('/', 1)
      word = splits[0]
      tag = splits[1]
      sentence_words.append(word)
      sentence_tags.append(tag)
    words.append(sentence_words)
    tags.append(sentence_tags)
  return words, tags


def generate_vocabulary_and_tag_files(training_data):
  training_tags_list = []
  training_words_list = []
  training_words_string = ''
  training_tags_string = ''
  for sentence in training_data:
    for word in sentence.strip().split():
      splits = word.rsplit('/', 1)
      word = splits[0]
      tag = splits[1]
      if word not in training_words_list:
        training_words_list.append(word)
        training_words_string += word + '\n'
      if tag not in training_tags_list:
        training_tags_list.append(tag)
        training_tags_string += tag + '\n'
  training_words_string += START_SYMBOL + STOP_SYMBOL
  training_tags_string += START_SYMBOL + STOP_SYMBOL
  return training_words_string, training_tags_string


def write_vocab_and_tags_to_txt(data_path, vocab, tags):
  with open(data_path + '/vocabulary.txt', "w") as f:
    f.write(vocab)
  with open(data_path + '/tags.txt', "w") as f:
    f.write(tags)


def main():
  TRAINING_DATA = '../data/train.txt'

  training_data = load_file(TRAINING_DATA)
  vocabulary_list, tag_list = generate_vocabulary_and_tag_files(training_data)
  write_vocab_and_tags_to_txt('../data', vocabulary_list, tag_list)


if __name__ == '__main__':
  main()