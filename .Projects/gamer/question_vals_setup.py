from main import question_num, dot


with open( f'{dot}/Data/question_vals.txt', 'w') as question_vals_file:
    question_vals_file.write(' | '.join(['0' for i in range(question_num)]))