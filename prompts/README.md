# Current Results on Inference Level Prompting on PaLM v2 models/text-bison-001

## Basic Prompting

We just put in the question as the prompt and see what the model generates.

### Addition

- Correct: 115
- Incorrect: 80
- Total: 195
- Accuracy: 0.5897435897435898

### Subtraction

- Correct: 356
- Incorrect: 152
- Total: 508
- Accuracy: 0.7007874015748031

### Multiplication

- Correct: 63
- Incorrect: 45
- Total: 108
- Accuracy: 0.5833333333333334

### Division

- Correct: 140
- Incorrect: 25
- Total: 165
- Accuracy: 0.8484848484848485

## Textual Prompting

We put in the question as the prompt and then give the equation to solve.

### Addition

- Correct: 115
- Incorrect: 80
- Total: 195
- Accuracy: 0.5897435897435898

### Subtraction

- Correct: 380
- Incorrect: 128
- Total: 508
- Accuracy: 0.7480314960629921

### Multiplication

- Correct: 53
- Incorrect: 55
- Total: 108
- Accuracy: 0.49074074074074076

### Division

- Correct: 142
- Incorrect: 23
- Total: 165
- Accuracy: 0.8606060606060606

## Scratch Prompting (1 Shot)

We put in a sample question and a `<scratch>` `<\scratch>` encasing how to do that operation.
Then, we ask the model to generate its own `<scratch>` `<\scratch>`, and use that to compute the answer.

### Addition

- Correct: 124
- Incorrect: 71
- Total: 195
- Accuracy: 0.6358974358974359

### Subtraction

- Correct: 450
- Incorrect: 58
- Total: 508
- Accuracy: 0.8858267716535433

### Multiplication

- Correct: 75
- Incorrect: 33
- Total: 108
- Accuracy: 0.6944444444444444

### Division

- Correct: 109
- Incorrect: 56
- Total: 165
- Accuracy: 0.6606060606060606
