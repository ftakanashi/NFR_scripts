#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
'''
    In a NFR corpus in which source sentences are enhanced with similar target translations,
    there might be multiple spans in a line. A concat symbol (like @@@) split spans.
    This scripts can selectively remove some spans in a line and remaining others.
    Also note that the script can flexibly deal with lines that do not have so much
    spans so that it can be adopted to a mixture of with_match and non_match lines.
'''

import argparse

def parse_args():

    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('corpus',
                        help='Path to the NFR corpus file.')

    parser.add_argument('-o', '--output', required=True,
                        help='Path to the output file.')

    parser.add_argument('--flag', required=True,
                        help='A string of 0 and 1 indicating whether to remove or remain'
                             'a span.')

    parser.add_argument('--concat-symbol', default='@@@',
                        help='DEFAULT: @@@\n The concat token.')

    opt = parser.parse_args()

    # validation
    for f in opt.flag:
        if f not in ('0', '1'):
            raise Exception(f'Invalid flag {f}.')

    return opt


def main():

    args = parse_args()

    flags = [c == '1' for c in args.flag]

    with open(args.corpus, 'r') as f:
        lines = [l.strip() for l in f]

    new_lines = []
    for l in lines:

        spans = l.split(args.concat_symbol)
        if len(spans) == 1:    # non_match lines
            new_lines.append(l)
            continue

        new_spans = []
        for i, span in enumerate(spans):
            try:
                flag = flags[i]
            except IndexError as e:
                # if flags are not enough to match every span, remain extra spans in default
                flag = True
            if flag:
                new_spans.append(span)

        new_lines.append(args.concat_symbol.join(new_spans))

    with open(args.output, 'w') as f:
        for l in new_lines:
            f.write(f'{l}\n')

if __name__ == '__main__':
    main()