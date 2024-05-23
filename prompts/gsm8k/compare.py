# compare results

# open results_{}.csv

import csv
import os
import argparse

arguments = argparse.ArgumentParser()
arguments.add_argument('-type', type=str, help='Type of prompt', required=True, choices=['scratch', 'basic', 'text', 'code', 'codeplustext'])

args = arguments.parse_args()
type_ = args.type

correct = 0
incorrect = 0
total = 0

correct = 0
incorrect = 0
total = 0

if type_ == 'text' or type_ == 'basic':
    with open('results_{}.csv'.format(type_), 'r') as f:
        for row in f:
            # skip the header
            if 'question' in row:
                continue
            try:
                row = row.strip().split(';')
                answer = row[-1]
                model_answer = row[-2]
                if answer in model_answer:
                    correct += 1
                else:
                    incorrect += 1
                total += 1
            except:
                continue


print(f"Correct: {correct}, Incorrect: {incorrect}, Total: {total}")
print(f"Accuracy: {correct/total}")