#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
'''
    Given a list of corpus files whose lines are exactly the same.
    Generate a new file in which lines are a concatenation of corresponding lines in the
    given file list.
    Note that the order of lines are determined by the order of the file list.
'''

import argparse

def parse_args():

    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('-f', '--files', nargs='+',
                        help='A list of files that to be merged in order.')
    parser.add_argument('-o', '--output',
                        help='Path to the output file.')

    parser.add_argument('--concat-symbol', default='@@@')

    args = parser.parse_args()
    assert len(args.files) >= 2

    if args.concat_symbol[0] != ' ':
        args.concat_symbol = f' {args.concat_symbol}'
    if args.concat_symbol[-1] != ' ':
        args.concat_symbol = f'{args.concat_symbol} '

    return args

def main():

    args = parse_args()

    lines_list = []
    for fn in args.files:
        with open(fn, 'r') as f:
            lines = [l.strip() for l in f]
            lines_list.append(lines)

    std_len = len(lines_list[0])
    for i,lines in enumerate(lines_list):
        assert len(lines) == std_len, f'Line number of {args.files[i]} seems to be inconsistent with {args.files[0]}'

    new_lines = []
    for i in range(std_len):
        new_lines.append(args.concat_symbol.join([lines[i] for lines in lines_list]))

    with open(args.output, 'w') as f:
        for new_line in new_lines:
            f.write(new_line + '\n')

if __name__ == '__main__':
    main()