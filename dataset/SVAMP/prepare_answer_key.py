import argparse
import os
import csv
import json

arguments = argparse.ArgumentParser()
arguments.add_argument('-file', type=str, help='File to parse')

args = arguments.parse_args()
file = args.file

# open JSONL file and get the data

with open(file) as jsonl_file:
    data = jsonl_file.read()
    data = data.split('\n')

# open a CSV file to write the data

with open('answers.csv', 'a') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(['question', 'answer'])

    # write the data
    for i in data:
        try:
            writer.writerow([json.loads(i)['Body'], json.loads(i)['Answer']])
        except:
            print('Error')
            print(i)
            continue