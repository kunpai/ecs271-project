import json
import os

with open('data.csv', 'w') as f:
    f.write('question;answer;equation\n')

for line in open('data.jsonl'):
    try:
        data = json.loads(line)
        question = data['question'].strip()
        answer = data['answer'].split('####')[1].strip()
        equation = data['answer'].split('<<')[1].split('>>')[0].strip()
        with open('data.csv', 'a') as f:
            f.write(question + ';' + answer + ';' + equation + '\n')
    except:
        print(data)
        continue