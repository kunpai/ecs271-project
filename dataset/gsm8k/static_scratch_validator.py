import csv

import sys
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.metrics import edit_distance
# Increase the CSV field size limit
csv.field_size_limit(sys.maxsize)

correct = 0
total = 0
incorrect = 0
row_count = 0

rows = []

# Open csv file
with open('data_sampled_addition.csv', 'r') as f:
    # Count the number of rows
    row_count = sum(1 for line in f)
    # append every row to a list
    # Reset file pointer to beginning
    f.seek(0)

    # Create a CSV reader object
    for line in f:
        rows.append(line)

old_rows = []

with open('results_scratch_small.csv', 'r') as f:
    for row in f:
        old_rows.append(row)

print("Total rows:", len(rows))
print(len(old_rows))

for i, row in enumerate(rows):
    gold = row.split('#')[0]
    for i, old_row in enumerate(old_rows):
        if gold in old_row:
            if old_rows[i].split('@')[0] in row.split('#')[0]:
                if old_rows[i].split('@')[-1] in row.split('#')[1]:
                    correct += 1
                else:
                    incorrect += 1
            else:
                incorrect += 1
            total += 1

print('Correct:', correct)
print('Incorrect:', incorrect)
print('Total:', total)


blue_scores = []

# reorder to match the first element of the rows
old_rows = sorted(old_rows, key=lambda x: x.split('@')[0])
rows = sorted(rows, key=lambda x: x.split('#')[0])

# remove the extra rows if there are more in either list
if len(rows) > len(old_rows):
    rows = rows[:len(old_rows)]
elif len(old_rows) > len(rows):
    old_rows = old_rows[:len(rows)]

# do BLEU score matching
for i, row in enumerate(rows):
    print("Generation: {}".format(row))
    print("Gold: {}".format(old_rows[i]))
    print("Edit distance: {}".format(edit_distance(row, old_rows[i])))
    print("BLEU score: {}".format(sentence_bleu([row], old_rows[i], smoothing_function=SmoothingFunction().method4)))
    blue_scores.append(sentence_bleu([row], old_rows[i], smoothing_function=SmoothingFunction().method4))

print("Average BLEU score: {}".format(sum(blue_scores) / len(blue_scores)))
