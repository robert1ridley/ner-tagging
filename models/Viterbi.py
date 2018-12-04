import math


class Viterbi(object):

  def __init__(self, in_transition_probabilities, in_emission_probabilities, in_word_tags_set,
               in_unique_tags, in_bigram_counts, in_observations):
    self.emission_probabilities = in_emission_probabilities
    self.transition_probabilities = in_transition_probabilities
    self.word_tags_set = in_word_tags_set
    self.observation_tag_probability = {}
    self.index_tag_key = None
    self.unique_tags = in_unique_tags
    self.bigram_counts = in_bigram_counts
    self.observations = in_observations
    self.no_tags = len(in_unique_tags)


  def calc_backpointers(self, observations, idx, item):
    if idx == 1:
      return 0.0
    if (idx, item) in self.observation_tag_probability:
      return self.observation_tag_probability[idx, item][0]
    if observations[idx - 1] not in self.word_tags_set:
      first_item = self.unique_tags
    else:
      first_item = self.word_tags_set[observations[idx - 1]]
    if observations[idx - 2] not in self.word_tags_set:
      second_item = self.unique_tags
    else:
      second_item = self.word_tags_set[observations[idx - 2]]
    max_prob = float('-inf')
    pointer = "*"
    for first_ob_tag in first_item:
      for second_ob_tag in second_item:
        probability = 0.0
        if (second_ob_tag, first_ob_tag, item) in self.transition_probabilities:
          transition_prob = self.transition_probabilities[(second_ob_tag, first_ob_tag, item)]
        else:
          if (second_ob_tag, first_ob_tag) in self.bigram_counts:
            transition_prob = math.log(
              1.0 / float(self.bigram_counts[(second_ob_tag, first_ob_tag)] + self.no_tags))
          else:
            transition_prob = math.log(1.0 / float(self.no_tags))
        if (observations[idx], item) not in self.emission_probabilities:
          transition_prob = 0.0
          probability = self.calc_backpointers(observations, idx - 1, first_ob_tag) + transition_prob
        else:
          probability = self.calc_backpointers(observations, idx - 1, first_ob_tag) + \
                        self.emission_probabilities[(observations[idx], item)] + transition_prob
        if max_prob < probability:
          max_prob = probability
          pointer = first_ob_tag
    self.observation_tag_probability[idx, item] = (max_prob, (idx - 1, pointer))
    return max_prob


  def calc_viterbi(self):
    tag_list = []
    observations = self.observations
    for observation in observations:
      max_prob = float('-inf')
      self.observation_tag_probability = {}
      obs_length = len(observation)
      if observation[obs_length - 1] not in self.word_tags_set:
        obs_and_tag = self.unique_tags
      else:
        obs_and_tag = self.word_tags_set[observation[obs_length - 1]]
      for item in obs_and_tag:
        current_probability = self.calc_backpointers(observation, obs_length - 1, item)
        if max_prob < current_probability:
          max_prob = current_probability
          self.index_tag_key = (obs_length - 1, item)
      tag_sets = []
      while self.index_tag_key[0] >= 2:
        if self.index_tag_key[1] != '*':
          tag_sets.insert(0, self.index_tag_key[1])
        else:
          tag_sets.insert(0, 'O')
        self.index_tag_key = self.observation_tag_probability[self.index_tag_key][1]
      tag_list.append(tag_sets)
    return tag_list