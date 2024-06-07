import json
import os

with open('data_small.csv', 'w') as f:
    f.write('question#answer#equation#scratch#simplified_equation\n')

def generate_scratch(equation):
    operation = ""
    if '+' in equation:
        operation = 'add'
    elif '-' in equation:
        operation = 'subtract'
    elif '*' in equation:
        return None, None, None, 'multiply'
    elif '/' in equation:
        return None, None, None, 'divide'

    if equation == '1/0.5':
        equation = '1*2'
        operation = 'multiply'

    if equation == '30*1/5':
        equation = '30/5'
        operation = 'divide'

    if equation == '40/.4':
        equation = '400/4'
        operation = 'divide'

    if equation == '1/.05':
        equation = '100/5'
        operation = 'divide'

    if equation == '15000/0.4':
        equation = '150000/4'
        operation = 'divide'

    if equation == '112/.5':
        equation = '112*2'
        operation = 'multiply'

    scratch = ""

    if operation == 'add':
        try:
            addend1, addend2 = equation.split('+')
            addend1 = [i for i in addend1 if i not in ['(', ')']]
            addend2 = [i for i in addend2 if i not in ['(', ')']]
            addend1 = ''.join(addend1)
            addend2 = ''.join(addend2)
        except:
            try:
                addend1, addend2, addend3 = equation.split('+')
                addend1 = str(addend1)
                addend2 = str(addend2)
                addend3 = str(addend3)
                addend1 = [i for i in addend1 if i not in ['(', ')']]
                addend2 = [i for i in addend2 if i not in ['(', ')']]
                addend3 = [i for i in addend3 if i not in ['(', ')']]
                addend1 = ''.join(addend1)
                addend2 = ''.join(addend2)
                addend3 = ''.join(addend3)
                addend2 = float(addend2) + float(addend3)
                addend2 = str(addend2)
            except:
                addend1, addend2, addend3, addend4 = equation.split('+')
                addend1 = str(addend1)
                addend2 = str(addend2)
                addend3 = str(addend3)
                addend4 = str(addend4)
                addend1 = [i for i in addend1 if i not in ['(', ')']]
                addend2 = [i for i in addend2 if i not in ['(', ')']]
                addend3 = [i for i in addend3 if i not in ['(', ')']]
                addend4 = [i for i in addend4 if i not in ['(', ')']]
                addend1 = ''.join(addend1)
                addend2 = ''.join(addend2)
                addend3 = ''.join(addend3)
                addend4 = ''.join(addend4)
                addend2 = float(addend2) + float(addend3) + float(addend4)
                addend2 = str(addend2)

        if '+' in addend1:
            addend1 = addend1.split('+')
            addend1 = sum([int(round(float(i))) for i in addend1])
        elif '-' in addend1:
            addend1 = addend1.split('-')
            addend1 = int(round(float(addend1[0])) - int(round(float(addend1[1]))))
        elif '*' in addend1:
            addend1 = addend1.split('*')
            addend1 = int(round(float(addend1[0])) * int(round(float(addend1[1]))))
        else:
            addend1 = int(round(float(addend1)))

        if '+' in addend2:
            addend2 = addend2.split('+')
            addend2 = sum([int(round(float(i))) for i in addend2])
        elif '-' in addend2:
            addend2 = addend2.split('-')
            addend2 = int(round(float(addend2[0])) - int(round(float(addend2[1]))))
        elif '*' in addend2:
            addend2 = addend2.split('*')
            addend2 = int(round(float(addend2[0])) * int(round(float(addend2[1]))))
        else:
            addend2 = int(round(float(addend2)))

        num1_str = str(addend1)
        num2_str = str(addend2)

        if len(num1_str) > len(num2_str):
            num2_str = "0" * (len(num1_str) - len(num2_str)) + num2_str
        elif len(num2_str) > len(num1_str):
            num1_str = "0" * (len(num2_str) - len(num1_str)) + num1_str

        scratch = "<scratch>"

        if '-' in num1_str or '-' in num2_str:
            if '-' in num1_str:
                num1_str = num1_str[1:]
                borrow = 0
                total_diff = ""

                for i in range(len(num1_str)-1, -1, -1):
                    digit1 = int(num1_str[i])
                    digit2 = int(num2_str[i])
                    current_diff = digit1 - digit2 - borrow

                    if current_diff < 0:
                        borrow = 1
                        current_diff += 10
                    else:
                        borrow = 0

                    scratch += "Subtracting {} and {} gives {}; ".format(digit1, digit2, current_diff)
                    if borrow:
                        scratch += "Borrow of 1 from the next place value. "

                    total_diff = str(current_diff) + total_diff

                scratch += "The result is {}.</scratch>".format(total_diff)

            elif '-' in num2_str:
                num2_str = num2_str[1:]
                borrow = 0
                total_diff = ""

                for i in range(len(num1_str)-1, -1, -1):
                    digit1 = int(num1_str[i])
                    digit2 = int(num2_str[i])
                    current_diff = digit2 - digit1 - borrow

                    if current_diff < 0:
                        borrow = 1
                        current_diff += 10
                    else:
                        borrow = 0

                    scratch += "Subtracting {} and {} gives {}; ".format(digit2, digit1, current_diff)
                    if borrow:
                        scratch += "Borrow of 1 from the next place value. "

                    total_diff = str(current_diff) + total_diff

                scratch += "The result is {}.</scratch>".format(total_diff)
        else:
            carry = 0
            total_sum = ""

            for i in range(len(num1_str)-1, -1, -1):
                digit1 = int(num1_str[i])
                digit2 = int(num2_str[i])

                current_sum = digit1 + digit2 + carry

                scratch += " Adding {} and {} at digit level. Current carry is {}; ".format(digit1, digit2, carry)
                scratch += "{} plus {} plus carry gives {}; ".format(digit1, digit2, current_sum)

                if current_sum > 9:
                    carry = 1
                    result_digit = current_sum - 10
                    scratch += "new carry is {}; result is {}. ".format(carry, result_digit)
                else:
                    carry = 0
                    result_digit = current_sum
                    scratch += "new carry is NaN; result is {}. ".format(result_digit)

                total_sum = str(result_digit) + total_sum

            if carry:
                total_sum = str(carry) + total_sum
                scratch += "0 plus 0 plus carry gives {}; ".format(carry)

            scratch += "The overall result is {}</scratch>".format(total_sum)

        # prompt = d['Body'] + ' ' + d['Question'] + ' '
        # prompt += 'Equation: <equation> ' + str(addend1) + ' + ' + str(addend2) + '</equation>'
        # prompt += ' ' + scratch

    if operation == 'subtract':
        try:
            minuend, subtrahend = equation.split('-')
            # remove parentheses inside the strings
            minuend = [i for i in minuend if i not in ['(', ')']]
            subtrahend = [i for i in subtrahend if i not in ['(', ')']]
            minuend = ''.join(minuend)
            subtrahend = ''.join(subtrahend)
        except:
            try:
                # basically there are two subtractions in the equation
                minued, subtrahend, subtrahend2 = equation.split('-')
                # convert all to strings
                minuend = str(minued)
                subtrahend = str(subtrahend)
                subtrahend2 = str(subtrahend2)
                minuend = [i for i in minuend if i not in ['(', ')']]
                subtrahend = [i for i in subtrahend if i not in ['(', ')']]
                subtrahend2 = [i for i in subtrahend2 if i not in ['(', ')']]
                minuend = ''.join(minuend)
                subtrahend = ''.join(subtrahend)
                subtrahend2 = ''.join(subtrahend2)
                # trim out apostrophes (single quotes and double quotes)
                # subtract subtahehnd2 from subtrahend
                subtrahend = float(subtrahend) - float(subtrahend2)
                subtrahend = str(subtrahend)
            except:
                minuend, subtrahend, subtrahend2, subtrahend3 = equation.split('-')
                minuend = str(minuend)
                subtrahend = str(subtrahend)
                subtrahend2 = str(subtrahend2)
                subtrahend3 = str(subtrahend3)
                minuend = [i for i in minuend if i not in ['(', ')']]
                subtrahend = [i for i in subtrahend if i not in ['(', ')']]
                subtrahend2 = [i for i in subtrahend2 if i not in ['(', ')']]
                subtrahend3 = [i for i in subtrahend3 if i not in ['(', ')']]
                minuend = ''.join(minuend)
                subtrahend = ''.join(subtrahend)
                subtrahend2 = ''.join(subtrahend2)
                subtrahend3 = ''.join(subtrahend3)
                subtrahend = float(subtrahend) - float(subtrahend2) - float(subtrahend3)
                subtrahend = str(subtrahend)

        if '+' in minuend:
            minuend = minuend.split('+')
            minuend = sum([int(round(float(i))) for i in minuend])
        elif '*' in minuend:
            minuend = minuend.split('*')
            minuend = int(round(float(minuend[0])) * int(round(float(minuend[1]))))
        elif '/' in minuend:
            minuend = minuend.split('/')
            minuend = int(round(float(minuend[0])) / int(round(float(minuend[1]))))
        else:
            minuend = int(round(float(minuend)))

        if '+' in subtrahend:
            subtrahend = subtrahend.split('+')
            subtrahend = sum([int(round(float(i))) for i in subtrahend])
        elif '*' in subtrahend:
            subtrahend = subtrahend.split('*')
            subtrahend = int(round(float(subtrahend[0])) * int(round(float(subtrahend[1]))))
        elif '/' in subtrahend:
            subtrahend = subtrahend.split('/')
            subtrahend = int(round(float(subtrahend[0])) / int(round(float(subtrahend[1]))))
        else:
            subtrahend = int(round(float(subtrahend)))

        # scratch = " {} - {}; ".format(minuend, subtrahend)
        scratch = ""
        num1_str = str(minuend)
        num2_str = str(subtrahend)

        if '-' in num1_str:
            num1_str = num1_str[1:]
        if '-' in num2_str:
            num2_str = num2_str[1:]

        # pad the shorter number with zeros on the left
        if len(num1_str) > len(num2_str):
            num2_str = "0" * (len(num1_str) - len(num2_str)) + num2_str
        elif len(num2_str) > len(num1_str):
            num1_str = "0" * (len(num2_str) - len(num1_str)) + num1_str

        # Initialize borrow
        borrow = 0
        total_diff = ""

        # Initialize variables
        scratch = ""
        total_diff = ""
        borrow = 0

        # Loop through each digit from right to left
        for i in range(len(num1_str) - 1, -1, -1):
            digit1 = int(num1_str[i])
            digit2 = int(num2_str[i])

            # Adjust for borrow if necessary
            if borrow:
                digit1 -= 1
                borrow = 0

            # Determine if we need to borrow
            if digit1 < digit2:
                borrow = 1

            # Calculate the current difference
            current_diff = digit1 - digit2 if digit1 >= digit2 else digit1 + 10 - digit2

            # Build the scratch string with details
            scratch += "Subtracting {} from {} at digit level; ".format(digit2, digit1)
            # scratch += "Current digit1: {}; digit2: {}; ".format(digit1, digit2)
            scratch += " {} {} {}; ".format(digit1, '>=' if digit1 >= digit2 else '<', digit2)
            scratch += " Borrow: {}; ".format(borrow)
            scratch += "{} - {} = {}. move one place left; ".format(digit1 + 10 if borrow else digit1, digit2, digit1 - digit2 if digit1 >= digit2 else digit1 + 10 - digit2)
            if borrow:
                scratch += "{} becomes {}; ".format(num1_str[i-1], int(num1_str[i-1])-1)
            else:
                scratch += "{} remains {}; ".format(num1_str[i-1], num1_str[i-1])
            # scratch += "Current difference: {}. ".format(current_diff)
            # scratch += "Updated digit1: {}. ".format(digit1-1 if borrow else digit1)

            total_diff = str(current_diff) + total_diff

        # Adjust the final result to remove leading zero if necessary
        total_diff = total_diff.lstrip('0')
        result = int(total_diff)
        scratch += "final result: {}.".format(result)
        scratch = "<scratch>" + scratch + "</scratch>"

        # prompt = d['Body'] + ' ' + d['Question'] + ' '
        # prompt += 'Equation: <equation> ' + str(minuend) + ' - ' + str(subtrahend) + '</equation>'
        # prompt += ' ' + "<scratch>" + scratch + "</scratch>"
        # prompts.append(prompt)

    if operation == 'multiply':
        factor1, factor2 = equation.split('*')

        if '+' in factor1:
            factor1 = factor1.split('+')
            factor1[0] = factor1[0][1:]
            factor1[-1] = factor1[-1][:-1]
            factor1 = sum([int(round(float(i))) for i in factor1])
        elif '-' in factor1:
            factor1 = factor1.split('-')
            factor1[0] = factor1[0][1:]
            factor1[-1] = factor1[-1][:-1]
            factor1 = int(round(float(factor1[0])) - int(round(float(factor1[1]))))
        elif '/' in factor1:
            factor1 = factor1.split('/')
            factor1[0] = factor1[0][1:]
            factor1[-1] = factor1[-1][:-1]
            factor1 = int(round(float(factor1[0])) / int(round(float(factor1[1]))))
        else:
            factor1 = int(round(float(factor1)))

        if '+' in factor2:
            factor2 = factor2.split('+')
            factor2[0] = factor2[0][1:]
            factor2[-1] = factor2[-1][:-1]
            factor2 = sum([int(round(float(i))) for i in factor2])
        elif '-' in factor2:
            factor2 = factor2.split('-')
            factor2[0] = factor2[0][1:]
            factor2[-1] = factor2[-1][:-1]
            factor2 = int(round(float(factor2[0])) - int(round(float(factor2[1]))))
        elif '/' in factor2:
            factor2 = factor2.split('/')
            factor2[0] = factor2[0][1:]
            factor2[-1] = factor2[-1][:-1]
            factor2 = int(round(float(factor2[0])) / int(round(float(factor2[1]))))
        else:
            factor2 = int(round(float(factor2)))


        # Generate prompt
        # prompt = d['Body'] + ' ' + d['Question'] + ' '
        # prompt += 'Equation: <equation> ' + d['Equation'] + '</equation>'

        # Describe the scratch work, i.e., how to perform the multiplication
        product = factor1 * factor2
        # Initialize scratch explanation
        scratch = "Multiplication is repeated addition. ".format(factor1, factor2, product, factor1, factor2)

        # Perform repeated addition
        partial_product = 0
        for _ in range(factor2):
            scratch += "Adding {} to the current total, which is {}. ".format(factor1, partial_product)
            partial_product += factor1
        # Conclude the explanation with the final product
        scratch += "After repeating this process {} times, we get the final result, which is {}. ".format(factor2, product)

        scratch = "<scratch>" + scratch + "</scratch>"


    if operation == 'divide':
        dividend, divisor = equation.split('/')
        # dividend might be a complex expression, so we need to evaluate it
        # convert to int to remove the decimal point
        # split dividend by possible operators
        if '+' in divisor:
            divisor = divisor.split('+')
            # remove first and last characters, which are parentheses
            divisor[0] = divisor[0][1:]
            divisor[-1] = divisor[-1][:-1]
            divisor = sum([int(round(float(i))) for i in divisor])
        elif '-' in divisor:
            divisor = divisor.split('-')
            divisor[0] = divisor[0][1:]
            divisor[-1] = divisor[-1][:-1]
            divisor = int(round(float(divisor[0]))) - int(round(float(divisor[1])))
        elif '*' in divisor:
            divisor = divisor.split('*')
            divisor[0] = divisor[0][1:]
            divisor[-1] = divisor[-1][:-1]
            divisor = int(round(float(divisor[0]))) * int(round(float(divisor[1])))
        else:
            divisor = int(round(float(divisor)))

        if '+' in dividend:
            dividend = dividend.split('+')
            dividend[0] = dividend[0][1:]
            dividend[-1] = dividend[-1][:-1]
            dividend = sum([int(round(float(i))) for i in dividend])
        elif '-' in dividend:
            dividend = dividend.split('-')
            dividend[0] = dividend[0][1:]
            dividend[-1] = dividend[-1][:-1]
            dividend = int(round(float(dividend[0]))) - int(round(float(dividend[1])))
        elif '*' in dividend:
            dividend = dividend.split('*')
            dividend[0] = dividend[0][1:]
            dividend[-1] = dividend[-1][:-1]
            dividend = int(round(float(dividend[0]))) * int(round(float(dividend[1])))
        # convert divisor to int
        else:
            dividend = int(round(float(dividend)))
        # prompt = d['Body'] + ' ' + d['Question'] + ' '
        # prompt = prompt + 'The dividend is {} and the divisor is {}. '.format(dividend, divisor)
        # describe the scratch work, i.e., how to perform the division
        # keep track of the quotient and remainder do the division until remainder is less than divisor
        quotient = 0
        remainder = dividend
        scratch = ""
        while remainder >= divisor:
            quotient += 1
            scratch += "To divide {} by {}, we subtract {} from {} to get a remainder of {}. ".format(remainder, divisor, divisor, remainder, remainder - divisor)
            scratch += "The quotient is now {}. ".format(quotient)
            if remainder - divisor == 0 or remainder - divisor < divisor:
                scratch += "We cannot divide {} by {} anymore. ".format(remainder - divisor, divisor)
                scratch += "This is because the remainder is less than the divisor, i.e., {} < {}. ".format(remainder - divisor, divisor)
                scratch += "The final quotient is {}. ".format(quotient)
                scratch += "The final remainder is {}. ".format(remainder - divisor)
                break
            else:
                scratch += "We need to divide {} by {} again. ".format(remainder - divisor, divisor)
                scratch += "This is because the remainder is greater than the divisor, i.e., {} > {}. ".format(remainder - divisor, divisor)
                scratch += "The remainder is now {}. ".format(remainder - divisor)
            remainder = remainder - divisor
        scratch = "<scratch>" + scratch + "</scratch>"
        # prompt = prompt + ' ' + "<scratch>" + scratch + "</scratch>"
    if operation == 'add':
        print('add')
        number1 = int(addend1)
        number2 = int(addend2)
    elif operation == 'subtract':
        print('subtract')
        number1 = int(minuend)
        number2 = int(subtrahend)
    return scratch, number1, number2, operation

addition_gsm8k = []
subtraction_gsm8k = []
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
        print(equation)
        scratch, number1, number2, operation = generate_scratch(equation)
        if operation == 'divide' or operation == 'multiply':
            continue
        if operation == 'add':
            simplified_equation = str(number1) + ' + ' + str(number2)
        elif operation == 'subtract':
            simplified_equation = str(number1) + ' - ' + str(number2)
        if scratch is None:
            scratch = '<scratch>Failed to generate scratch work</scratch>'
            continue
        print(operation)
        # equation = data['answer'].split('<<')[1].split('>>')[0].strip()
        if operation == 'add':
            addition_gsm8k.append((question, answer, equation, scratch, simplified_equation))
        elif operation == 'subtract':
            subtraction_gsm8k.append((question, answer, equation, scratch, simplified_equation))
        # with open('data_small.csv', 'a') as f:
        #     f.write(question + '#' + answer + '#' + equation + '#' + scratch + '#' + simplified_equation + '\n')
    except Exception as e:
        print(e)
        print(line)
        continue

print(len(addition_gsm8k))
print(len(subtraction_gsm8k))
# sample out 200 questions from each operation
import random
random.seed(42)
random.shuffle(addition_gsm8k)
random.shuffle(subtraction_gsm8k)
addition_gsm8k = addition_gsm8k[:400]
subtraction_gsm8k = subtraction_gsm8k[:400]

with open('data_sampled_addition.csv', 'w') as f:
    f.write('question#answer#equation#scratch#simplified_equation\n')
    for row in addition_gsm8k:
        f.write(row[0] + '#' + row[1] + '#' + row[2] + '#' + row[3] + '#' + row[4] + '\n')

with open('data_sampled_subtraction.csv', 'w') as f:
    f.write('question#answer#equation#scratch#simplified_equation\n')
    for row in subtraction_gsm8k:
        f.write(row[0] + '#' + row[1] + '#' + row[2] + '#' + row[3] + '#' + row[4] + '\n')
