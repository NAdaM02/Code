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
        ouput.append("0")


    if not is_input_divisible:
        print("NEM")
    print(" ".join(output_numbers))


whole_sequence:tuple = tuple(input())

def test_if_sequence_is_mutant(sequence):
    ACGT_count_list = []

for part_sequence_start in range(0, len(whole_sequence)-2):
    for part_sequence_end in range(len(whole_sequence)-1, i, -1):

