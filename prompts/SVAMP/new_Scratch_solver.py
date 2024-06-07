import argparse
import json
import os
import pprint
import google.generativeai as palm
from time import sleep
import csv
from dotenv import load_dotenv

load_dotenv()

palm.configure(api_key=os.environ['API'])
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name
print(model)

arguments = argparse.ArgumentParser()
arguments.add_argument('-file', type=str, help='File to parse')
arguments.add_argument('-top5', type=bool, help='Whether to use top 5 or not', default=False, required=True)
arguments.add_argument('--scratch', type=bool, help='Whether it is a scratch-style prompt or not', default=True, required=False)
args = arguments.parse_args()
file = args.file
scratch = args.scratch
top5 = args.top5

last_line = 0
if os.path.exists('answers_similar'+ file.replace('.csv', '') + '.csv'):
    # get the last line number
    with open('answers_similar'+ file.replace('.csv', '') + '.csv') as f:
        for i, l in enumerate(f):
            last_line = i
    # last_line = i + 1

with open(file) as csv_file:
    data = csv_file.read()
    # split by new line
    data = data.split('\n')
    # truncate the data to the last line
    data = data[last_line:]

ctr = 0

if scratch == True:
    if top5 == False:
        if os.path.exists('answers_similar'+ file.replace('.csv', '') + '.csv') is False:
            with open('answers_similar'+ file.replace('.csv', '') + '.csv', 'a') as f:
                # write header
                f.write('question#scratch#answer\n')
    else:
        if os.path.exists('answers_similar'+ file.replace('.csv', '') + '.csv') is False:
            with open('answers_similar'+ file.replace('.csv', '') + '.csv', 'a') as f:
                # write header
                f.write('equation#closest_equation#scratch#answer\n')

for i in data:
    if top5 == False:
        if i == "equation#carry#full_prompt#closest_equation1#closest_bleu_score1#closest_distance1#closest_prompt1#closest_equation2#closest_bleu_score2#closest_distance2#closest_prompt2#closest_equation3#closest_bleu_score3#closest_distance3#closest_prompt3#closest_equation4#closest_bleu_score4#closest_distance4#closest_prompt4#closest_equation5#closest_bleu_score5#closest_distance5#closest_prompt5#closest_equation6#closest_bleu_score6#closest_distance6#closest_prompt6#closest_equation7#closest_bleu_score7#closest_distance7#closest_prompt7#closest_equation8#closest_bleu_score8#closest_distance8#closest_prompt8#closest_equation9#closest_bleu_score9#closest_distance9#closest_prompt9#closest_equation10#closest_bleu_score10#closest_distance10#closest_prompt10":
            continue
        i = i.split("#")
        gold_example = i[6]
        # trim out <scratch> and </scratch> tags from i and everything in between
        question = i[2].split('<scratch>')[0]
        print(question)
        print(gold_example)
        prompt = "Look at this example: " + gold_example + "\n"
        prompt += "Generate a <scratch> and </scratch> section for the following problem: " + question
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
            print('Failed to get answer for ' + question)
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
            print('Failed to get answer for ' + question)
            completion.result = 'Failed to get answer'
        print(completion.result)
        answer = completion.result.replace('\n', ' ')
        scratch_section = scratch_section.replace('\n', ' ')
        # any other newline characters
        scratch_section = scratch_section.replace('\n', ' ')
        with open('answers_similar'+ file.replace('.csv', '') + '.csv', 'a') as f:
            f.write(question + '#' + scratch_section + '#' + answer + '\n')
        sleep(1)
        ctr = 0
    else:
        if i == "equation#carry#full_prompt#closest_equation1#closest_bleu_score1#closest_distance1#closest_prompt1#closest_equation2#closest_bleu_score2#closest_distance2#closest_prompt2#closest_equation3#closest_bleu_score3#closest_distance3#closest_prompt3#closest_equation4#closest_bleu_score4#closest_distance4#closest_prompt4#closest_equation5#closest_bleu_score5#closest_distance5#closest_prompt5#closest_equation6#closest_bleu_score6#closest_distance6#closest_prompt6#closest_equation7#closest_bleu_score7#closest_distance7#closest_prompt7#closest_equation8#closest_bleu_score8#closest_distance8#closest_prompt8#closest_equation9#closest_bleu_score9#closest_distance9#closest_prompt9#closest_equation10#closest_bleu_score10#closest_distance10#closest_prompt10":
            continue
        i = i.split("#")
        equation = i[0]
        top1 = i[3]
        top2 = i[7]
        top3 = i[11]
        top4 = i[15]
        top5 = i[19]

        print(equation)
        print(top1)
        print(top2)
        print(top3)
        print(top4)
        print(top5)
        question = i[2].split('<scratch>')[0]

        prompt = "Given the following equation: <equation>" + equation + "<equation>\n" + "What is the closest equation to it, semantically?. Consider which equation you would like to learn how to solve to help solve the aforementioned equation. Your options are: <equation>" + top1 + "<equation>, <equation>" + top2 + "<equation>, <equation>" + top3 + "<equation>, <equation>" + top4 + "<equation>, <equation>" + top5 + "<equation>"
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
            print('Failed to get answer for ' + equation)
            completion.result = 'Failed to get answer'
        print(completion.result)
        answer = completion.result.replace('\n', ' ')
        # find which equation model chose
        if top1 in answer:
            closest_equation = top1
        elif top2 in answer:
            closest_equation = top2
        elif top3 in answer:
            closest_equation = top3
        elif top4 in answer:
            closest_equation = top4
        elif top5 in answer:
            closest_equation = top5
        else:
            closest_equation = top1

        if closest_equation == top1:
            gold_example = i[6]
        elif closest_equation == top2:
            gold_example = i[10]
        elif closest_equation == top3:
            gold_example = i[14]
        elif closest_equation == top4:
            gold_example = i[18]
        elif closest_equation == top5:
            gold_example = i[22]

        prompt = "Look at this example: " + gold_example + "\n"
        prompt += "Generate a <scratch> and </scratch> section for the following problem: " + question
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
            print('Failed to get answer for ' + question)
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
            print('Failed to get answer for ' + question)
            completion.result = 'Failed to get answer'
        print(completion.result)
        answer = completion.result.replace('\n', ' ')
        scratch_section = scratch_section.replace('\n', ' ')
        # any other newline characters
        scratch_section = scratch_section.replace('\n', ' ')
        with open('answers_similar'+ file.replace('.csv', '') + '.csv', 'a') as f:
            f.write(question + '#' + closest_equation + "#" + scratch_section + '#' + answer + '\n')
        sleep(1)
        ctr = 0

