from utils import get_pairs, load_file
from nltk import bigrams, trigrams

class Hmm(object):

    def __init__(self):
        pass


def calculate_emissions(sentences):
    emission_count = {}
    term = 'ONEGRAM '
    for sentence in sentences[:500]:
        for pair in sentence:
            if term + pair[0] + ' ' + pair[1] not in emission_count.keys():
                emission_count[term + pair[0] + ' ' + pair[1]] = 1
            else:
                emission_count[term + pair[0] + ' ' + pair[1]] += 1
    return emission_count


def calc_bigram_emissions(sequence_sets):
  bigram_emission_dict = {}
  term = 'BIGRAM '
  for seq in sequence_sets:
    biGr = list(bigrams(seq))
    for item in biGr:
      if term + item[0] + ' ' + item[1] not in bigram_emission_dict.keys():
        bigram_emission_dict[term + item[0] + ' ' + item[1]] = 1
      else:
        bigram_emission_dict[term + item[0] + ' ' + item[1]] += 1
  return bigram_emission_dict


def calc_trigram_emissions(sequence_sets):
  trigram_emission_dict = {}
  term = 'TRIGRAM '
  for seq in sequence_sets:
    trGr = list(trigrams(seq))
    for item in trGr:
      if term + item[0] + ' ' + item[1] + ' ' + item[2] not in trigram_emission_dict.keys():
        trigram_emission_dict[term + item[0] + ' ' + item[1] + ' ' + item[2]] = 1
      else:
        trigram_emission_dict[term + item[0] + ' ' + item[1] + ' ' + item[2]] += 1
  return trigram_emission_dict


def get_tag_seqs(sentences):
    sets = []
    for sentence in sentences:
        tags = []
        for pair in sentence:
            tags.append(pair[1])
        sets.append(tags)
    return sets


def write_emissions_to_text(_words, _bigrams, _trigrams, pathname):
  text = ''
  for key in _words:
    text += key + ' ' + str(_words[key]) + '\n'
  for key in _bigrams:
    text += key + ' ' + str(_bigrams[key]) + '\n'
  for key in _trigrams:
    text += key + ' ' + str(_trigrams[key]) + '\n'
  with open(pathname, "w") as f:
    f.write(text)


def main():
    data = load_file('../data/train.txt')
    sentences = get_pairs(data)
    tag_seqs = get_tag_seqs(sentences)
    onegram_emissions = calculate_emissions(sentences)
    bigram_emissions = calc_bigram_emissions(tag_seqs)
    trigram_emissions = calc_trigram_emissions(tag_seqs)
    write_emissions_to_text(onegram_emissions, bigram_emissions, trigram_emissions, '../data/emission_counts.txt')


if __name__ == '__main__':
    main()