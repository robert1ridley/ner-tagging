def load_vocabulary_and_tags(path_name):
  vocabulary_file = open(path_name + 'vocabulary.txt', 'r')
  vocabulary_list = vocabulary_file.readlines()
  vocabulary_file.close()

  tags_file = open(path_name + 'tags.txt', 'r')
  tags_list = tags_file.readlines()
  tags_file.close()
  return vocabulary_list, tags_list


def generate_vocab_dictionary(vocabulary):
  vocabulary_dictionary = {}
  count = 0
  for word in vocabulary:
    word = word.strip()
    vocabulary_dictionary[word] = count
    count += 1
  return vocabulary_dictionary


def generate_tag_dictionary(tags):
  tag_dictionary = {}
  count = 0
  for tag in tags:
    tag = tag.strip()
    tag_dictionary[tag] = count
    count += 1
  return tag_dictionary


def get_training_data(training_data):
  full_data = []
  for sentence in training_data:
    current_sentence_words = []
    current_sentence_tags = []
    for word in sentence.strip().split():
      splits = word.rsplit('/', 1)
      current_sentence_words.append(splits[0])
      current_sentence_tags.append(splits[1])
    full_data.append((current_sentence_words, current_sentence_tags))
  return full_data


def get_pairs(training_data):
  START = '*'
  STOP = "STOP"
  start_seq = (START, START)
  stop_seq = (STOP, STOP)
  pairs = []
  for sentence in training_data:
    single_sentence = [start_seq, start_seq]
    for word in sentence.strip().split():
      splits = word.rsplit('/', 1)
      single_sentence.append((splits[0], splits[1]))
    single_sentence.append(stop_seq)
    pairs.append(single_sentence)
  return pairs


def load_file(filepath):
  infile = open(filepath, 'r')
  data = infile.readlines()
  infile.close()
  return data


def get_states(pathname):
  states = load_file(pathname)
  state_list = []
  for state in states:
    state_list.append(state.strip())
  return state_list


def main():
  vocabulary, tags = load_vocabulary_and_tags('../data/')
  vocabulary_dictionary = generate_vocab_dictionary(vocabulary)
  tag_dictionary = generate_tag_dictionary(tags)


if __name__ == '__main__':
    main()