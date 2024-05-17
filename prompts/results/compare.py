import argparse
import os
import csv

arguments = argparse.ArgumentParser()
arguments.add_argument('-operation', type=str, help='Operation to evaluate', required=True, choices=['addition', 'subtraction', 'multiplication', 'division'])
arguments.add_argument('-type', type=str, help='Type of prompt', required=True, choices=['scratch', 'basic', 'text'])

args = arguments.parse_args()
operation = args.operation

# get the answer key
answer_key = []

with open('answer_key/answers_{}.csv'.format(operation)) as f:
    reader = csv.reader(f)
    for row in reader:
        answer_key.append(row)

# get the model results

results = []
with open('model/answers_{}_{}.csv'.format(args.type, operation)) as f:
    reader = csv.reader(f)
    for row in reader:
        results.append(row)

# remove first element from both lists
answer_key = answer_key[1:]
results = results[1:]

# evaluate the results
correct = 0
incorrect = 0
total = 0

for i in range(len(answer_key)):
    print("Answer key: {}".format(answer_key[i][1]))
    print("Model: {}".format(results[i][-1]))
    if results[i][-1] in answer_key[i][1]:
        correct += 1
    else:
        incorrect += 1
    total += 1

print("Correct: {}".format(correct))
print("Incorrect: {}".format(incorrect))
print("Total: {}".format(total))
print("Accuracy: {}".format(correct / total))

# write the results to a file
with open('results/{}_{}_results.csv'.format(args.type, operation), 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['question', 'correct', 'model'])
    for i in range(len(answer_key)):
        writer.writerow([answer_key[i][0], answer_key[i][1], results[i][-1]])