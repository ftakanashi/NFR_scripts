#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
    Given an original alignment file with possible alignments
    and an alignment file produced by fast_align.
    Generate a new file containing all the sure alignments in the
    original one and fast_align alignments which overlap with
    the original possible alignments
'''

import argparse


def parse_args():
    parser = argparse.ArgumentParser(
    '''
        Given an original alignment file with possible alignments
        and an alignment file produced by fast_align.
        Generate a new file containing all the sure alignments in the
        original one and fast_align alignments which overlap with
        the original possible alignments
    '''
    )

    parser.add_argument('original', help='Original alignment file containing sure and possible alignments.'
                                         'Default CONCAT for sure and possible alignments are \'-\' and \'p\'.')
    parser.add_argument('fa', help='Alignment file produced by fast_align.')

    parser.add_argument('-o', '--output', required=True)

    parser.add_argument('--original-start-from-one', action='store_true', help='If the original alignments starts from'
                                                                               'one, add this option to make it '
                                                                               'consistent with fast_align alignments.')
    parser.add_argument('--maintain-possible-concat', action='store_true', help='Possible concat \'p\' is defaultly '
                                                                                'replaced by sure concat. Add this '
                                                                                'option to maintain it.')

    opt = parser.parse_args()

    return opt


def adapt_start_from_one(align_rows):
    new_rows = []
    for align_row in align_rows:
        new_aligns = []
        for align in align_row:
            if '-' in align:
                concat = '-'
            else:
                concat = 'p'
            a, b = align.split(concat)
            a, b = int(a), int(b)
            a -= 1
            b -= 1
            new_aligns.append(f'{a}{concat}{b}')
        new_rows.append(new_aligns)
    return new_rows

def main():

    opt = parse_args()

    with open(opt.original, 'r') as f:
        original_lines = [l.strip() for l in f]
        ori_aligns = [l.split() for l in original_lines]
        if opt.original_start_from_one:
            ori_aligns = adapt_start_from_one(ori_aligns)

    with open(opt.fa, 'r') as f:
        fa_lines = [l.strip() for l in f]
        fa_aligns = [l.split() for l in fa_lines]

    new_rows = []
    for i, ori_align_row in enumerate(ori_aligns):
        fa_align_row = fa_aligns[i]
        filtered_align = []
        for ori_align in ori_align_row:
            if '-' in ori_align or ori_align.replace('p', '-') in fa_align_row:
                if not opt.maintain_possible_concat:
                    ori_align = ori_align.replace('p', '-')
                filtered_align.append(ori_align)

        new_rows.append(' '.join(filtered_align))

    with open(opt.output, 'w') as f:
        f.write('\n'.join(new_rows))

if __name__ == '__main__':
    main()