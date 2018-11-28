START_SYMBOL = '*\n'
STOP_SYMBOL = 'STOP\n'

def load_training_data():
  infile = open('../data/dev.txt', 'r')
  data = infile.readlines()
  infile.close()
  return data


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
  training_data = load_training_data()
  vocabulary_list, tag_list = generate_vocabulary_and_tag_files(training_data)
  write_vocab_and_tags_to_txt('../data', vocabulary_list, tag_list)


if __name__ == '__main__':
  main()