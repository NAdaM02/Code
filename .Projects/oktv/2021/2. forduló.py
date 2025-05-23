def ELSO_FELADAT():
    def f(x:int) -> int:
        y = (x - x%10)//10 - (x%10)*11
        return y

    input_num:int = int(input())

    n:int = f(input_num)

    is_input_divisible = False
    output_numbers = []

    while n > 0:
        output_numbers.append(str(n))
        n = f(n)
        if n % 37 == 0:
            print("IGEN")
            is_input_divisible = True

    if n == 0:
        output_numbers.append("0")


    if not is_input_divisible:
        print("NEM")
    print(" ".join(output_numbers))


def MASODIK_FELADAT():
    whole_sequence:tuple = tuple(input())
    whole_sequence_len = len(whole_sequence)

    def sequence_is_mutant(sequence):
        mutant = False
        ACGT_count_dict = {'A':0, 'C':0, 'G':0, 'T':0}

        for val in sequence:
            ACGT_count_dict[val] += 1
        
        for val in ('A','C','G','T'):
            if ACGT_count_dict[val]*2 >= len(sequence):
                return True
        
        return False

    found = False
    for length in range(whole_sequence_len, -1, -1):
        
        for start in range(0, whole_sequence_len-length):
            part_sequence = whole_sequence[start : (start+length+1)]
            if sequence_is_mutant(part_sequence):
                print(len(part_sequence))
                found = True
                break
        
        if found: break


def HARMADIK_FELADAT():
    num_of_lengths, num_of_questions = map(int, input().split())
    lengths = tuple(map(int, input().split()))

    answers = [0 for i in range(num_of_questions)]

    for q in range(num_of_questions):
        a, b = map(int, input().split())
        for c in lengths:
            if a+b>c and a+c>b and b+c>a:
                answers[q] += 1

    for answer in answers: print(answer)


#def NEGYEDIK_FELADAT():
height, width, piece_count = map(int, input().split())

pieces:list = []
for piece in range(piece_count):
    row, col = map(int, input().split())
    pieces.append((row, col))

pass_count = 0

import os
from time import sleep as wait
def visualize_field(r_positions, p_position, height, width):
    field_map = [['.' for i in range(width)] for j in range(height)]
    for r_p in r_positions:
        field_map[r_p[0]-1][r_p[1]-1] = '×'
    field_map[p_position[0]-1][p_position[1]-1] = 'o'

    for row in field_map:
        print(" ".join(row))

#os.system('cls')
while 0 < len(pieces):
    pass_count += 1
    passing_position = [1, 1]
    while passing_position != [height, width]:
        #print('pass:', pass_count)
        #visualize_field(pieces, passing_position, height, width)
        moved = False
        for i in range(len(pieces)):
            if pieces[i][0] == passing_position[0] and passing_position[1] < pieces[i][1]: # in same row
                passing_position[1] = pieces[i][1]
                del(pieces[i])
                moved = True
                break
        if not moved:
            for i in range(len(pieces)):
                if pieces[i][1] == passing_position[1] and passing_position[0] < pieces[i][0]: # in same column
                    passing_position[0] = pieces[i][0]
                    del(pieces[i])
                    moved = True
                    break
        if not moved:
            if passing_position[0] == height:
                passing_position[1] = width
            elif passing_position[1] < width:
                passing_position[1] += 1
            else:
                passing_position = [height, width]
        #wait(0.5)
        #os.system('cls')
    
    #print('pass:', pass_count)
    #visualize_field(pieces, passing_position, height, width)
    #wait(0.5)
    #os.system('cls')

print(pass_count)
