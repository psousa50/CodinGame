inputs = [
    "17630 9000",
    "3",
    "3 0",
    "3 0",
    "18",
    "0 1 9795 1989 0 0 -1 -1 -1 -1 -1",
    "1 1 5214 6068 0 0 -1 -1 -1 -1 -1",
    "2 1 9417 2747 0 0 -1 -1 -1 -1 -1",
    "3 2 11482 6279 0 0 -1 -1 -1 -1 -1",
    "4 2 11444 6417 0 0 -1 -1 -1 -1 -1",
    "5 2 11822 6016 0 0 -1 -1 -1 -1 -1",
    "6 0 12693 3219 0 0 10 277 287 0 2",
    "7 0 4937 5781 0 0 4 -277 -287 0 1",
    "8 0 12591 4787 0 0 10 -16 399 0 0",
    "9 0 5039 4213 0 0 8 16 -399 0 0",
    "10 0 5890 1298 0 0 10 -325 233 0 1",
    "11 0 11740 7702 0 0 10 325 -233 0 2",
    "12 0 12527 2783 0 0 10 -32 398 0 0",
    "13 0 5103 6217 0 0 6 32 -398 0 0",
    "14 0 7771 409 0 0 11 -261 302 0 0",
    "15 0 9859 8591 0 0 11 261 -302 0 0",
    "16 0 14159 65 0 0 11 336 216 0 0",
    "17 0 3471 8935 0 0 11 -336 -216 0 0",
    "-1 -1",
]

current_input_pointer = 0


def input():
    global current_input_pointer
    i = inputs[current_input_pointer]
    current_input_pointer += 1
    if current_input_pointer >= len(inputs):
        current_input_pointer = 0
    return i
