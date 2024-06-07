
import csv
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from nltk.metrics import edit_distance

txt_file = r"scratch_addition_newsep.txt"

csv_file = r"equation_addition.csv"

in_txt = csv.reader(open(txt_file, "r"), delimiter = '\n')

# open csv file
with open(csv_file, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='#')
    writer.writerow(["equation", "carry", "full_prompt"])

for row in in_txt:
    equation = row[0].split('<equation>')[1].split('</equation>')[0]
    equation = equation.replace(' ', '')
    equation = equation.replace('.0', '')
    equation = equation.replace('(' , '')
    equation = equation.replace(')' , '')
    # figure out if a carry is needed in the addition
    carry = False
    if '+' in equation:
        num1, num2 = equation.split('+')
        if len(num1) > len(num2):
            # append 0s to the front of num2
            num2 = '0' * (len(num1) - len(num2)) + num2
        else:
            # append 0s to the front of num1
            num1 = '0' * (len(num2) - len(num1)) + num1
        #equation = num1 + '+' + num2
        try:
            if int(num1[-1]) + int(num2[-1]) >= 10:
                carry = True
            elif len(num1) > 1 and len(num2) > 1 and int(num1[-2]) + int(num2[-2]) >= 10:
                carry = True
            elif len(num1) > 2 and len(num2) > 2 and int(num1[-3]) + int(num2[-3]) >= 10:
                carry = True
        except:
            carry = False
    elif '-' in equation:
        try:
            num1, num2 = equation.split('-')
            if len(num1) > len(num2):
                # append 0s to the front of num2
                num2 = '0' * (len(num1) - len(num2)) + num2
            else:
                # append 0s to the front of num1
                num1 = '0' * (len(num2) - len(num1)) + num1
            equation = num1 + '-' + num2
            if int(num1[-1]) < int(num2[-1]):
                carry = True
            elif len(num1) > 1 and len(num2) > 1 and int(num1[-2]) < int(num2[-2]):
                carry = True
            elif len(num1) > 2 and len(num2) > 2 and int(num1[-3]) < int(num2[-3]):
                carry = True
        except:
            carry = False

    # replace the equation in row[0] between the <equation> tags with the new equation
    # row[0] = row[0].split('<equation>')[0] + '<equation> ' + equation + '</equation>' + row[0].split('</equation>')[1]
    with open(csv_file, 'a', newline='') as f:
        writer = csv.writer(f, delimiter='#')
        writer.writerow([equation, carry, row[0]])

new_lines = []
with open(csv_file, 'r') as f:
    rows = f.readlines()

    for i, row in enumerate(rows):
        if "equation#carry#full_prompt" in row:
            new_row = row + "closest_equation1#closest_bleu_score1#closest_distance1#closest_prompt1#closest_distance1#closest_equation2#closest_bleu_score2#closest_distance2#closest_prompt2#closest_distance2#closest_equation3#closest_bleu_score3#closest_distance3#closest_prompt3#closest_distance3#closest_equation4#closest_bleu_score4#closest_distance4#closest_prompt4#closest_distance4#closest_equation5#closest_bleu_score5#closest_distance5#closest_prompt5#closest_distance5#closest_equation6#closest_bleu_score6#closest_distance6#closest_prompt6#closest_distance6#closest_equation7#closest_bleu_score7#closest_distance7#closest_prompt7#closest_distance7#closest_equation8#closest_bleu_score8#closest_distance8#closest_prompt8#closest_distance8#closest_equation9#closest_bleu_score9#closest_distance9#closest_prompt9#closest_distance9#closest_equation10#closest_bleu_score10#closest_distance10#closest_prompt10#closest_distance10\n"
            new_lines.append(new_row)
            continue

        # Split the row into its components
        equation, carry, full_prompt = map(str.strip, row.split('#'))

        # Create a list of each character in the equation plus the carry value
        candidate = list(equation) + [str(carry)]

        print(f"Processing row {i}: {candidate}")

        closest_equation = None
        closest_bleu_score = 0
        closest_distance = 0
        closest_prompt = None

        blue_scores = []
        # Iterate through other rows, skipping the current row
        for j, other_row in enumerate(rows):
            if j == i or "equation#carry#full_prompt" in other_row:
                continue

            # Process the other rows as needed
            other_equation, other_carry, other_full_prompt = map(str.strip, other_row.split('#'))
            other_candidate = list(other_equation) + [str(other_carry)]

            # Here you can add any logic to compare or process `candidate` and `other_candidate`
            print(f"Comparing with row {j}: {other_candidate}")

            # Calculate the BLEU score with weights considering up to 3-grams
            bleu_score = sentence_bleu([other_candidate], candidate, weights=(1, 0, 0, 0), smoothing_function=SmoothingFunction().method1)
            print(f"BLEU score: {bleu_score}")

            # Calculate the edit distance
            distance = edit_distance(other_candidate, candidate)
            print(f"Edit Distance: {distance}")

            # Update the closest match if needed
            if bleu_score > closest_bleu_score or (bleu_score == closest_bleu_score and distance < closest_distance):
                closest_equation = other_equation
                closest_bleu_score = bleu_score
                closest_distance = distance
                closest_prompt = other_full_prompt

            blue_scores.append((j, bleu_score, distance, other_full_prompt, other_equation))

        # find all the rows with the top 10 of BLEU scores and lowest edit distance
        blue_scores.sort(key=lambda x: (x[1], -x[2]), reverse=True)
        # print(f"Top 10% of closest BLEU scores:")
        # for k in range(10):
        #     print(f"Row {blue_scores[k][0]}: {blue_scores[k][3]}")
        #     print(f"BLEU score: {blue_scores[k][1]}")
        #     print(f"Edit Distance: {blue_scores[k][2]}")
        #     print()

        # print(f"Closest match for row {i}:")
        # print(f"Equation: {closest_equation}")
        # print(f"BLEU score: {closest_bleu_score}")
        # print(f"Edit Distance: {closest_distance}")
        # print(f"Full Prompt: {closest_prompt}")

        print()

        # write top 10 closest matches to the csv file
        # closest_equation1#closest_bleu_score1#closest_distance1#closest_prompt1
        new_row = row.strip() + '#' + blue_scores[0][4] + '#' + str(blue_scores[0][1]) + '#' + str(blue_scores[0][2]) + '#' + blue_scores[0][3] + '#' + blue_scores[1][4] + '#' + str(blue_scores[1][1]) + '#' + str(blue_scores[1][2]) + '#' + blue_scores[1][3] + '#' + blue_scores[2][4] + '#' + str(blue_scores[2][1]) + '#' + str(blue_scores[2][2]) + '#' + blue_scores[2][3] + '#' + blue_scores[3][4] + '#' + str(blue_scores[3][1]) + '#' + str(blue_scores[3][2]) + '#' + blue_scores[3][3] + '#' + blue_scores[4][4] + '#' + str(blue_scores[4][1]) + '#' + str(blue_scores[4][2]) + '#' + blue_scores[4][3] + '#' + blue_scores[5][4] + '#' + str(blue_scores[5][1]) + '#' + str(blue_scores[5][2]) + '#' + blue_scores[5][3] + '#' + blue_scores[6][4] + '#' + str(blue_scores[6][1]) + '#' + str(blue_scores[6][2]) + '#' + blue_scores[6][3] + '#' + blue_scores[7][4] + '#' + str(blue_scores[7][1]) + '#' + str(blue_scores[7][2]) + '#' + blue_scores[7][3] + '#' + blue_scores[8][4] + '#' + str(blue_scores[8][1]) + '#' + str(blue_scores[8][2]) + '#' + blue_scores[8][3] + '#' + blue_scores[9][4] + '#' + str(blue_scores[9][1]) + '#' + str(blue_scores[9][2]) + '#' + blue_scores[9][3] + '\n'

        # new_row = row.strip() + '#' + closest_equation + '#' + str(closest_bleu_score) + '#' + str(closest_distance) + '#' + closest_prompt + '\n'
        new_lines.append(new_row)

with open(csv_file, 'w') as f:
    f.writelines(new_lines)



