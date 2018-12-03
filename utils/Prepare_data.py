class Prepare_data(object):

  def __init__(self):
    self.tag_set = []
    self.pairs = []
    self.word_tag_appearances = {}


  def is_tag_in_tag_set(self, tag):
    if tag not in self.tag_set:
      self.tag_set.append(tag)
    return self.tag_set


  def are_word_and_tag_in_dictionary(self, word, tag):
    if word not in self.word_tag_appearances:
      self.word_tag_appearances[word] = [tag]
    elif tag not in self.word_tag_appearances[word]:
      self.word_tag_appearances[word].append(tag)


  def get_pairs(self, training_data):
    START = '*'
    start_seq = (START, START)
    pairs = []
    for sentence in training_data:
      single_sentence = []
      for word in sentence.strip().split():
        splits = word.rsplit('/', 1)
        single_sentence.append((splits[0], splits[1]))
        self.is_tag_in_tag_set(splits[1])
        self.are_word_and_tag_in_dictionary(splits[0], splits[1])
      single_sentence.insert(0, start_seq)
      pairs.append(single_sentence)
    self.pairs = pairs
    return pairs