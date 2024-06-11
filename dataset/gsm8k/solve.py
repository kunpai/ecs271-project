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
arguments.add_argument('-type', type=str, help='Type of prompt', required=True, choices=['scratch', 'basic', 'text', 'code', 'codeplustext'])
arguments.add_argument('--scratch', type=bool, help='Whether it is a scratch-style prompt or not', default=False, required=False)
args = arguments.parse_args()
scratch = args.scratch

# with open('results.csv', 'w') as f:
#     f.write('question,model_answer,answer\n')

#open data.csv
with open('data_small.csv', 'r') as f:
    data = f.read()
    data = data.split('\n')

data = data[1:]

type_ = args.type



last_line = 0
if os.path.exists('results.csv'):
    # get the last line number
    with open('results.csv') as f:
        for i, l in enumerate(f):
            last_line = i
    # last_line = i + 1

# with open(file) as txt_file:
#     data = txt_file.read()
#     # split by new line
#     data = data.split('\n')
#     # truncate the data to the last line

data = data[last_line:]

# print(data[0])

ctr = 0

# if type_ == 'basic':
#     for i in data:
#         prompt = "Solve this problem: " + i.split(';')[0]
#         completion = palm.generate_text(
#             model=model,
#             prompt=prompt,
#             temperature=0,
#             max_output_tokens=500,
#         )
#         while completion.result == '' or completion.result == None and ctr < 5:
#             sleep(2)
#             completion = palm.generate_text(
#                 model=model,
#                 prompt=prompt,
#                 temperature=0,
#                 max_output_tokens=500,
#             )
#             ctr += 1
#         if ctr == 5:
#             print('Failed to get answer for ' + i)
#             completion.result = 'Failed to get answer'
#         print(completion.result)
#         # remove new line characters
#         completion.result = completion.result.replace('\n', ' ')
#         with open('results.csv', 'a') as f:
#             f.write(i.split(';')[0] + ',' + completion.result + ',' + i.split(';')[1] + '\n')
#         sleep(1)
        # ctr = 0

if type_ == 'text' or type_ == 'basic':
    for i in data:
        prompt = "Solve this problem: " + i.split(';')[0] + "\n" + "Solve this equation for the answer: <equation>" + i.split(';')[2].split('=')[0] + " </equation>"
        print("Prompt:" + prompt)
        #prompt = "Solve this problem: " + i.split(';')[0]
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
        # remove new line characters
        prompt = prompt.replace('\n', ' ')
        completion.result = completion.result.replace('\n', ' ')
        print("Model Answer: " + completion.result)
        print("Actual Answer: " + i.split(';')[1])
        with open('results.csv', 'a') as f:
            f.write(prompt + ';' + completion.result + ';' + i.split(';')[1] + '\n')
        sleep(1)
        ctr = 0

# if scratch == False:
#     if os.path.exists('answers_'+ file.replace('.txt', '') + '.csv') is False:
#         with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
#             # write header
#             f.write('question,answer\n')

# if scratch == True:
#     if os.path.exists('answers_code'+ file.replace('.txt', '') + '.csv') is False:
#         with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
#             # write header
#             f.write('question,scratch,answer\n')


# if scratch == False:
#     for i in data:
#         prompt = "Solve this problem: " + i
#         completion = palm.generate_text(
#             model=model,
#             prompt=prompt,
#             temperature=0,
#             max_output_tokens=500,
#         )
#         while completion.result == '' or completion.result == None and ctr < 5:
#             sleep(2)
#             completion = palm.generate_text(
#                 model=model,
#                 prompt=prompt,
#                 temperature=0,
#                 max_output_tokens=500,
#             )
#             ctr += 1
#         if ctr == 5:
#             print('Failed to get answer for ' + i)
#             completion.result = 'Failed to get answer'
#         print(completion.result)
#         # remove new line characters
#         completion.result = completion.result.replace('\n', ' ')
#         with open('answers_'+ file.replace('.txt', '') + '.csv', 'a') as f:
#             f.write(i + ',' + completion.result + '\n')
#         sleep(1)
#         ctr = 0

if type_ == 'scratch':

    for i in data:
        # trim out <scratch> and </scratch> tags from i and everything in between
        equation = i.split(';')[2]
        # add spaces around the operators
        equation = equation.replace('+', ' + ') if '+' in equation else equation.replace('-', ' - ')
        if '+' in equation:
            gold_example = "A waiter had some customers. After 9 customers left he still had 12 customers. How many customers did he have at the start? Equation: <equation> 9 + 12</equation> <scratch> Adding 9 and 2 at digit level. Current carry is 0; 9 plus 2 plus carry gives 11; new carry is 1; result is 1.  Adding 0 and 1 at digit level. Current carry is 1; 0 plus 1 plus carry gives 2; new carry is NaN; result is 2. The overall result is 21</scratch>"
            #gold_example = "Equation: <equation> 9 + 12</equation> <scratch> Adding 9 and 2 at digit level. Current carry is 0; 9 plus 2 plus carry gives 11; new carry is 1; result is 1.  Adding 0 and 1 at digit level. Current carry is 1; 0 plus 1 plus carry gives 2; new carry is NaN; result is 2. The overall result is 21</scratch>" + "\n"
            # gold_example += "Equation: <equation> 42 + 20</equation> <scratch> Adding 2 and 0 at digit level. Current carry is 0; 2 plus 0 plus carry gives 2; new carry is 0; result is 2.  Adding 4 and 2 at digit level. Current carry is 0; 4 plus 2 plus carry gives 6; new carry is NaN; result is 6. The overall result is 62</scratch>"
        elif '-' in equation:
            # gold_example = 'Mary is baking a cake. The recipe calls for 12 cups of flour and 5 cups of sugar. She already put in some cups of flour. If she still needs 2 more cups of flour How many cups of flour did she put in? Equation: <equation> 12 - 2</equation> <scratch>Subtracting 2 from 2 at digit level;  2 >= 2;  Borrow: 0; 2 - 2 = 0. move one place left; 1 remains 1; Subtracting 0 from 1 at digit level;  1 >= 0;  Borrow: 0; 1 - 0 = 1. move one place left; 2 remains 2; final result: 10.</scratch>'
            gold_example = "Equation: <equation> 12 - 2</equation> <scratch>Subtracting 2 from 2 at digit level;  2 >= 2;  Borrow: 0; 2 - 2 = 0. move one place left; 1 remains 1; Subtracting 0 from 1 at digit level;  1 >= 0;  Borrow: 0; 1 - 0 = 1. move one place left; 2 remains 2; final result: 10.</scratch>"
        prompt = "Look at this example: " + gold_example + "\n"
        # prompt += "Generate a methodology and place it between <scratch> and </scratch> tags for the following problem: " + i.split(';')[0] + "Equation: <equation>" + equation + " </equation>"
        prompt += "Generate a methodology and place it between <scratch> and </scratch> tags for the following problem: " + i.split(';')[0]
        print("Prompt:" + prompt)
        print("Equation:" + equation)
       #prompt = "Write Python code to solve this problem: " + i.split(';')[0]
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
        prompt = "Now solve this problem: " + i.split(';')[0] + "\n" + "Given the following methodology: " + scratch_section
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
        print(prompt)
        print(completion.result)
        answer = completion.result.replace('\n', ' ')
        scratch_section = scratch_section.replace('\n', ' ')
        # any other newline characters
        scratch_section = scratch_section.replace('\n', ' ')
        with open('results.csv', 'a') as f:
            f.write(i.split(';')[0] + '@' + scratch_section + '@' + completion.result + '@' + i.split(';')[1] + '\n')
        sleep(1)
        sleep(1)
        ctr = 0