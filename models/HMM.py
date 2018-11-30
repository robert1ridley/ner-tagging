def is_in_emissions_dict(word, emissions_dict):
  for k, v in emissions_dict.items():
    if word in v.keys():
      return True
  return False


def viterbi(sentence, transition, emission):
  sentence.insert(0, '*')
  sentence.insert(0, '*')
  sentence.append('STOP')
  paths = []

  # Calc initial paths
  index = 2
  initial_word = sentence[index]
  word_in_dict = is_in_emissions_dict(initial_word, emission)
  if not word_in_dict:
    initial_word = '_RARE_'
  for item in transition:
    if item[0] == '*' and item[1] == '*':
      current_tag = item[2]
      if current_tag in emission.keys():
        if initial_word in emission[current_tag].keys():
          probability = float(emission[current_tag][initial_word]) * float(transition[item])
          paths.append([(item, probability)])
  index += 1

  # Calc remaining paths
  while index < len(sentence):
    current_word = sentence[index]
    point_count = 0
    for point in paths:
      tag1 = point[-1][0][1]
      tag2 = point[-1][0][2]
      prob = point[-1][1]
      best_set = ()
      max_prob = -100
      word_in_dict = is_in_emissions_dict(current_word, emission)
      if not word_in_dict:
        current_word = '_RARE_'
      for tran in transition:
        if tran[0] == tag1 and tran[1] == tag2:
          current_tag = tran[2]
          if current_tag in emission.keys():
            if current_word in emission[current_tag].keys():
              probability = float(emission[current_tag][current_word]) * float(transition[tran])
              if probability*prob > max_prob*prob:
                max_prob = probability
                best_set = tran
      if best_set != ():
        paths[point_count].append((best_set, max_prob))
      point_count += 1
    index += 1

  # ARGMAX to find most likely path
  best_prob_val = -100
  best_set = []
  for path in paths:
    prob_val = 0
    if len(path) == len(sentence)-2:
      for node in path:
        if prob_val == 0:
          prob_val = node[1]
        else:
          prob_val *= node[1]
    if prob_val > best_prob_val:
      best_prob_val = prob_val
      best_set = path

  final_set = []
  for item in best_set:
    tag = item[0][2]
    final_set.append(tag)
  return final_set[:-1]
