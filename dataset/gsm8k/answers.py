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
with open('answers_similarequation_addition_top5.csv', 'r') as f:
    # Count the number of rows
    row_count = sum(1 for line in f)
    # append every row to a list
    # Reset file pointer to beginning
    f.seek(0)
    
    # Create a CSV reader object
    for line in f:
        rows.append(line)


# Print the total number of rows
print("Total rows:", row_count)
print("Rows:", rows[0])

gold = []

with open('equation_addition.csv', 'r') as f:
    reader = csv.reader(f, delimiter = '#')
    for row in reader:
        gold.append(row[3])

print(len(gold))

for i, row in enumerate(rows):
    if row[-2] in gold[i]:
        correct += 1
    else:
        incorrect += 1
    total += 1

print('Correct:', correct)
print('Incorrect:', incorrect)
print('Total:', total)

# gold = []

# with open('equation_subtraction.csv', 'r') as f:
#     reader = csv.reader(f, delimiter = '#')
#     for row in reader:
#         gold.append(row[2])


# bleu_scores = []

# for i, row in enumerate(rows):
#     row = row.split('#')
#     print("Generation: {}".format(row[0]))
#     print("Gold: {}".format(gold[i]))
#     print("Edit distance: {}".format(edit_distance(row[0], gold[i])))
#     print("BLEU score: {}".format(sentence_bleu([row[0]], gold[i], smoothing_function=SmoothingFunction().method4)))
#     bleu_scores.append(sentence_bleu([row[0]], gold[i], smoothing_function=SmoothingFunction().method4))

# print("Average BLEU score: {}".format(sum(bleu_scores) / len(bleu_scores)))