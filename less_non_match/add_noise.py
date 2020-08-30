#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
    '''
        Given a corpus file, the script will add noise into it.
        Noise format: https://www.aclweb.org/anthology/D18-1045.pdf
    '''

import argparse
import random
import torch
from tqdm import tqdm


# the three following functions are copied from source script
def word_shuffle(s, sk):
    noise = torch.rand(len(s)).mul_(sk)
    perm = torch.arange(len(s)).float().add_(noise).sort()[1]
    return [s[i] for i in perm]


def word_dropout(s, wd):
    keep = torch.rand(len(s))
    res = [si for i, si in enumerate(s) if keep[i] > wd]
    if len(res) == 0:
        return [s[random.randint(0, len(s) - 1)]]
    return res


def word_blank(s, wb):
    keep = torch.rand(len(s))
    return [si if keep[i] > wb else 'Ж' for i, si in enumerate(s)]


def parse_args():
    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('corpus',
                        help='Path to the source corpus file.')

    parser.add_argument('-o', '--output',
                        help='Path to the output file.')

    parser.add_argument('-wd', help='Word dropout', default=0.1, type=float)
    parser.add_argument('-wb', help='Word blank', default=0.1, type=float)
    parser.add_argument('-sk', help='Shuffle k words', default=3, type=int)

    args = parser.parse_args()

    return args


def main():
    args = parse_args()

    with open(args.corpus, 'r') as f:
        lines = [l.strip() for l in f]

    new_lines = []
    for l in tqdm(lines, mininterval=0.5, ncols=50):
        tokens = l.split()
        if len(tokens) > 0:
            tokens = word_shuffle(tokens, args.sk)
            tokens = word_dropout(tokens, args.wd)
            tokens = word_blank(tokens, args.wb)

        new_lines.append(' '.join(tokens))

    with open(args.output, 'w') as f:
        for new_line in new_lines:
            f.write(new_line + '\n')


if __name__ == '__main__':
    main()
