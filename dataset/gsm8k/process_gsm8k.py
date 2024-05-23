import json
import os

with open('data.csv', 'w') as f:
    f.write('question;answer;equation\n')

for line in open('data.jsonl'):
    try:
        data = json.loads(line)
        question = data['question'].strip()
        answer = data['answer'].split('####')[1].strip()
        text = data['answer']
        start_index = text.rfind('<<') + 2
        end_index = text.rfind('>>')
        if start_index != -1 and end_index != -1 and start_index < end_index:
            equation = text[start_index:end_index].strip().split('=')[0].strip()
        else:
            equation = ''
        # equation = data['answer'].split('<<')[1].split('>>')[0].strip()
        with open('data.csv', 'a') as f:
            f.write(question + ';' + answer + ';' + equation + '\n')
    except:
        print(data)
        continue