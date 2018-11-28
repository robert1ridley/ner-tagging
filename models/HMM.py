from collections import defaultdict
from utils import get_pairs, load_file

class Hmm(object):

    def __init__(self):
        pass


def main():
    data = load_file('../data/train.txt')
    pairs = get_pairs(data)


if __name__ == '__main__':
    main()