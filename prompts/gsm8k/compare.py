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

with open('results_{}.csv'.format(type_), 'r') as f:
    for row in f:
        # skip the header
        if 'question' in row:
            continue
        try:
            row = row.strip().split(',')
            answer = row[-1]
            found = False
            # check if the model answer is in any other element in the row
            for i in row[1:-1]:
                if answer in i:
                    found = True
                    break
            if found:
                correct += 1
            else:
                incorrect += 1
            total += 1
        except:
            continue

print(f"Correct: {correct}, Incorrect: {incorrect}, Total: {total}")
print(f"Accuracy: {correct/total}")