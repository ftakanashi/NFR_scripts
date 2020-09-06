#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
'''
    By using a sentence transformer such as sentence-BERT, this script will encode
    a parallel corpus (src-tgt) to embeddings and save them to the disk.
    The embedding vectors will be arranged in the format of numpy arrays and saved
    as a text file using the method numpy.array.tofile.
    NOTE.
      In default settings, vectors with dimension of 512 and in format of float32 are 
      flattened before being written.
'''

import argparse
import numpy as np
from sentence_transformers import SentenceTransformer

def main():

    args = parse_args()

    print('Reading data...')
    with open(args.src, 'r') as f:
        src_lines = [l.strip() for l in f]
        if args.remove_bpe_in_corpus:
            src_lines = [l.replace('@@ ', '') for l in src_lines]

    with open(args.tgt, 'r') as f:
        tgt_lines = [l.strip() for l in f]
        if args.remove_bpe_in_corpus:
            tgt_lines = [l.replace('@@ ', '') for l in tgt_lines]

    assert len(src_lines) == len(tgt_lines)

    print('Loading S-BERT...')
    sbert = SentenceTransformer(args.model_dir)

    print('Calculating embedding...')
    src_embedding = sbert.encode(src_lines, show_progress_bar=True, batch_size=args.batch_size)
    tgt_embedding = sbert.encode(tgt_lines, show_progress_bar=True, batch_size=args.batch_size)

    print('Writing embeddings to file...')
    np.hstack(src_embedding).flatten().tofile(args.src_output)
    np.hstack(tgt_embedding).flatten().tofile(args.tgt_output)

def parse_args():
    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('-s', '--src', required=True,
                        help='Path to the source corpus file.')
    parser.add_argument('-t', '--tgt', required=True,
                        help='Path to the target corpus file.')

    parser.add_argument('-so', '--src-output', required=True,
                        help='Path to the embedding output file for source corpus.')
    parser.add_argument('-to', '--tgt-output', required=True,
                        help='Path to the embedding output file for target corpus.')

    parser.add_argument('--model-dir', default='sbert-model',
                        help='Directory in which the cached BERT model is saved. DEFAULT: "sbert-model"')
    parser.add_argument('--batch-size', default=128, type=int,
                        help='Batch size during encoding. DEFAULT: 128')
    parser.add_argument('--remove-bpe-in-corpus', action='store_true',
                        help='If there are BPE marks in corpus, remove them before input the sentences into SBERT.')

    args = parser.parse_args()
    return args

if __name__ == '__main__':
    main()