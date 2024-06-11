import argparse
import json
import os
import pprint
import google.generativeai as palm
from time import sleep
from dotenv import load_dotenv

load_dotenv()

palm.configure(api_key=os.environ['PALM_API_KEY'])
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

arguments = argparse.ArgumentParser()
arguments.add_argument('-file', type=str, help='File to parse')
arguments.add_argument('--scratch', type=bool, help='Whether it is a scratch-style prompt or not', default=False, required=False)
args = arguments.parse_args()
file = args.file
scratch = args.scratch

last_line = 0
if os.path.exists('answers_code'+ file.replace('.txt', '') + '.csv'):
    # get the last line number
    with open('answers_code'+ file.replace('.txt', '') + '.csv') as f:
        for i, l in enumerate(f):
            last_line = i
    # last_line = i + 1

with open(file) as txt_file:
    data = txt_file.read()
    # split by new line
    data = data.split('\n')
    # truncate the data to the last line
    data = data[last_line:]

print(data[0])

ctr = 0

if scratch == False:
    if os.path.exists('answers_'+ file.replace('.txt', '') + '.csv') is False:
        with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
            # write header
            f.write('question,answer\n')

if scratch == True:
    if os.path.exists('answers_code'+ file.replace('.txt', '') + '.csv') is False:
        with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
            # write header
            f.write('question,scratch,answer\n')


if scratch == False:
    for i in data:
        prompt = "Solve this problem: " + i
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=500,
        )
        while completion.result == '' or completion.result == None and ctr < 5:
            sleep(2)
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                max_output_tokens=500,
            )
            ctr += 1
        if ctr == 5:
            print('Failed to get answer for ' + i)
            completion.result = 'Failed to get answer'
        print(completion.result)
        # remove new line characters
        completion.result = completion.result.replace('\n', ' ')
        with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
            f.write(i + ',' + completion.result + '\n')
        sleep(1)
        ctr = 0

else:
    gold_example = data[3]

    for i in data:
        # trim out <scratch> and </scratch> tags from i and everything in between
        i = i.split('<scratch>')[0]
        prompt = "Look at this example: " + gold_example + "\n"
        prompt += "Generate a <scratch> and </scratch> section for the following problem: " + i
        # prompt = "Write Python code to solve this problem: " + i
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=500,
        )
        while completion.result == '' or completion.result == None and ctr < 5:
            sleep(2)
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                max_output_tokens=500,
            )
            ctr += 1
        if ctr == 5:
            print('Failed to get answer for ' + i)
            completion.result = 'Failed to get answer'
        print(completion.result)
        ctr = 0
        scratch_section = completion.result
        prompt = "Given the following methodology: " + scratch_section + "\n" + "What is the result?"
        # prompt = "Now, run this Python code: " + scratch_section + "\n" + "What is the output?"
        # remove new line characters
        completion = palm.generate_text(
            model=model,
            prompt=prompt,
            temperature=0,
            max_output_tokens=500,
        )
        while completion.result == '' or completion.result == None and ctr < 5:
            sleep(2)
            completion = palm.generate_text(
                model=model,
                prompt=prompt,
                temperature=0,
                max_output_tokens=500,
            )
            ctr += 1
        if ctr == 5:
            print('Failed to get answer for ' + i)
            completion.result = 'Failed to get answer'
        print(completion.result)
        answer = completion.result.replace('\n', ' ')
        scratch_section = scratch_section.replace('\n', ' ')
        # any other newline characters
        scratch_section = scratch_section.replace('\n', ' ')
        with open('answers_code'+ file.replace('.txt', '') + '.csv', 'a') as f:
            f.write(i + ',' + scratch_section + ',' + answer + '\n')
        sleep(1)
        ctr = 0