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


def main():
    data = load_file('../data/train.txt')
    sentences = get_pairs(data)
    calculate_emissions(sentences)


if __name__ == '__main__':
    main()