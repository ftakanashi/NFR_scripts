#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
'''
    Given a list of files. All the files are required to have same number of lines.
    Shuffle all lines of files but keeping all corresponding relationships between lines
    among files.
    NOTE: line shuffling will be done in-place
'''

import argparse
import random

def parse_args():

    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('-f', '--files', nargs='+',
                        help='List of files.')

    args = parser.parse_args()
    assert len(args.files) > 1

    return args

def main():

    args = parse_args()

    lines_list = []
    for fn in args.files:
        with open(fn, 'r') as f:
            lines = [l.strip() for l in f]
            lines_list.append(lines)

    std_len = len(lines_list[0])
    for i, lines in enumerate(lines_list):
        assert len(lines) == std_len, f'Line number of {args.files[i]} does not match {args.files[0]}'

    indices = list(range(std_len))
    random.shuffle(indices)

    for f_i, fn in enumerate(args.files):
        print(f'Writing {fn}...')
        lines = lines_list[f_i]
        with open(fn, 'w') as f:
            for i in indices:
                f.write(lines[i] + '\n')
if __name__ == '__main__':
    main()