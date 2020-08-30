#!/usr/bin/env python
# -*- coding:utf-8 -*-

NOTE = \
'''
    Given a JSON file which is organized in SQuAD 2.0 format, this script will read in the
    data and calculate the ratio of null-answer QAs among all QAs.
'''

import argparse
import json

def parse_args():
    parser = argparse.ArgumentParser(NOTE)

    parser.add_argument('json_file')

    args = parser.parse_args()

    return args


def main():

    args = parse_args()

    with open(args.json_file, 'r') as f:
        content = json.loads(f.read())

    qa_count = 0
    null_qa_count = 0

    for data in content['data']:
        for paragraph in data['paragraphs']:
            for qa in paragraph['qas']:
                if qa['is_impossible']:
                    null_qa_count += 1
                qa_count += 1

    print(f'Total QA Count: {qa_count}\nNull Answer QA Count: {null_qa_count}\n'
          f'Null Answer Ratio: {float(null_qa_count) / qa_count}')

if __name__ == '__main__':
    main()