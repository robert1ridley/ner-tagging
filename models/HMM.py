from utils import get_pairs, load_file

class Hmm(object):

    def __init__(self):
        pass


def calculate_emissions(sentences):
    emission_count = {}
    for sentence in sentences[:500]:
        for pair in sentence:
            if pair[0] not in emission_count.keys():
                emission_count[pair[0]] = 1
            else:
                emission_count[pair[0]] += 1
    return emission_count


def get_tag_seqs(sentences):
    sets = []
    for sentence in sentences:
        tags = []
        for pair in sentence:
            tags.append(pair[1])
        sets.append(tags)
    return sets


def main():
    data = load_file('../data/train.txt')
    sentences = get_pairs(data)
    calculate_emissions(sentences)
    tag_seqs = get_tag_seqs(sentences)
    print(tag_seqs[:20])


if __name__ == '__main__':
    main()