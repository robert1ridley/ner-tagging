def load_file(filepath):
  infile = open(filepath, 'r')
  data = infile.readlines()
  infile.close()
  return data


def get_test_data_sets(data):
  START = '*'
  sets = []
  for line in data:
    new_set = [START, START]
    set = line.split()
    for item in set:
      item = item.strip()
      new_set.append(item)
    sets.append(new_set)
  return sets


def get_dev_words_and_tags(data):
  START = '*'
  words = []
  tags = []
  for sentence in data:
    sentence_words = [START, START]
    sentence_tags = [START, START]
    for word in sentence.split():
      word = word.strip()
      splits = word.rsplit('/', 1)
      word = splits[0]
      tag = splits[1]
      sentence_words.append(word)
      sentence_tags.append(tag)
    words.append(sentence_words)
    tags.append(sentence_tags)
  return words, tags