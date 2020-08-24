#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
    Definition:
        Given a parallel corpus and a alignment file corresponding to it.
        If a word (source or target) does not have any alignment in alignment file, then it is
        a null-align word.
        Null align ratio = (total number of null-align words) / (total number of words)
'''

import argparse

def parse_args():
    parser = argparse.ArgumentParser(
    '''
        Definition:
            Given a parallel corpus and a alignment file corresponding to it.
            If a word (source or target) does not have any alignment in alignment file, then it is
            a null-align word.
            Null align ratio = (total number of null-align words) / (total number of words)
    '''
    )

    parser.add_argument('-s', '--src', required=True,
                        help='Path to the source corpus file.')
    parser.add_argument('-t', '--tgt', required=True,
                        help='Path to the target corpus file.')
    parser.add_argument('-a', '--align', required=True,
                        help='Path to the alignment file.')

    parser.add_argument('--align-start-from-one', action='store_true', default=False,
                        help='If the alignments in alignment file start from index 1, add this option.')

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

    with open(opt.src, 'r') as f:
        src_lines = [l.strip() for l in f]

    with open(opt.tgt, 'r') as f:
        tgt_lines = [l.strip() for l in f]

    with open(opt.align, 'r') as f:
        align_lines = [l.strip() for l in f]
        align_lines = [l.split() for l in align_lines]
        if opt.align_start_from_one:
            adapt_start_from_one(align_lines)

    total_word_count = 0
    null_word_count = 0
    for i, src_line in enumerate(src_lines):
        tgt_line = tgt_lines[i]
        src_len = len(src_line.strip().split())
        tgt_len = len(tgt_line.strip().split())
        total_word_count += src_len
        total_word_count += tgt_len

        aligns = align_lines[i]
        src_indices = set([])
        tgt_indices = set([])
        for align in aligns:
            concat = '-' if '-' in align else 'p'
            a, b = align.split(concat)
            a, b = int(a), int(b)
            src_indices.add(a)
            tgt_indices.add(b)

        for i in range(src_len):
            if i not in src_indices:
                null_word_count += 1

        for j in range(tgt_len):
            if j not in tgt_indices:
                null_word_count += 1

    ratio = float(null_word_count) / total_word_count
    print(f'Total Word Count: {total_word_count}\nNull Word Count: {null_word_count}')
    print(f'Null Align Ratio: {ratio}')

if __name__ == '__main__':
    main()