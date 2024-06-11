import argparse
import os
import csv
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.metrics import edit_distance

arguments = argparse.ArgumentParser()
arguments.add_argument('-operation', type=str, help='Operation to evaluate', required=True, choices=['addition', 'subtraction', 'multiplication', 'division'])
arguments.add_argument('-type', type=str, help='Type of prompt', required=True, choices=['scratch', 'basic', 'text', 'code', 'codeplustext', 'similarequation', 'similarequationpalm'])

args = arguments.parse_args()
operation = args.operation

prompts = []

with open('model/answers_{}_{}.csv'.format(args.type, operation)) as f:
        reader = csv.reader(f, delimiter='#')
        for row in reader:
            prompts.append(row[0] + " " + row[1])

# with open('model/answers_{}_{}_newsep.csv'.format(args.type, operation)) as f:
#         reader = csv.reader(f, delimiter=',')
#         for row in reader:
#             # everything except the last element
#             prompts.append(''.join(row[:-1]))

with open('../scratch_{}_newsep.txt'.format(operation), 'r') as f:
    data = f.read().split('\n')

prompts = prompts[1:]
print(len(prompts))
print(len(data))


bleu_scores = []

for i in range(len(prompts)):
    print("Generation: {}".format(prompts[i]))
    print("Gold: {}".format(data[i]))
    print("Edit distance: {}".format(edit_distance(prompts[i], data[i])))
    print("BLEU score: {}".format(sentence_bleu([prompts[i]], data[i], smoothing_function=SmoothingFunction().method4)))
    bleu_scores.append(sentence_bleu([prompts[i]], data[i], smoothing_function=SmoothingFunction().method4))

print("Average BLEU score: {}".format(sum(bleu_scores) / len(bleu_scores)))
