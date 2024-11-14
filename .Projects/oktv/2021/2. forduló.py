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


whole_sequence:tuple = tuple(input())
whole_sequence_len = len(whole_sequence)

def test_if_sequence_is_mutant(sequence):
    mutant = False
    ACGT_count_dict = {'A':0, 'C':0, 'G':0, 'T':0}

    for val in sequence:
        ACGT_count_dict[val] += 1
    
    for val in ('A','C','G','T'):
        if ACGT_count_dict[val]*2 >= len(sequence):
            return True
    
    return False
[0,1,2,3,4]
#j : 0, 0, 1, 0
#k : 4, 3, 4, 3
for part_sequence_start in range(0, whole_sequence_len):
    for change in range(0, whole_sequence_len-part_sequence_start):
        part_is_mutant = test_if_sequence_is_mutant(whole_sequence[part_sequence_start+change:part_sequence_end+1])
        if part_is_mutant:
            print(part_sequence_end-part_sequence_start)
            break
