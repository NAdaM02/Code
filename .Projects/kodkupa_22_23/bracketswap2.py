len_of_S = int(input())
S = input().replace(' ','')
S = list(S)

def swap(i,j):
    global S
    helper = S[i]
    S[i] = S[j]
    S[j] = helper

def Simplify(par_S, do_return = False) :
    simplified = 0
    simplifiable = True
    new_S = par_S
    print('from:', par_S, end=" to ")
    while simplifiable :
        simplifiable = False
        brackets = []
        for i in range(len_of_S):
            if not new_S[i] == '':
                brackets.append(i)
        i = 0
        while i + 1 < len(brackets) :
            if new_S[brackets[i]] == '(' and new_S[brackets[i+1]] == ')' :
                new_S[brackets[i]] = ''
                new_S[brackets[i+1]] = ''
                i += 1
                simplifiable = True
                simplified += 1
            i += 1
    print(new_S, simplified)
    if do_return :
        return simplified
    else:
        return new_S

done_S = ['' for i in range(len_of_S)]
print(S)
S = Simplify(S)
print('simplified:', S)
if S == done_S :
    print(0)
else :
    swaps = []
    while S != done_S :
        left_places = []
        right_places = []
        for i in range(len_of_S):
            if S[i] == '(' :
                left_places.append(i)
            elif S[i] == ')' :
                right_places.append(i)

        best_result = (('i', 'j'),0)
        for i in range(len(left_places)):
            for j in range(len(right_places)):
                print('###', S)
                S_before_change = S

                swap(left_places[i], right_places[j])
                print(left_places[i], right_places[j], end=' ')
                simplicity_score = Simplify(S,True)
                if  simplicity_score > best_result[1] :
                    best_result = ((left_places[i], right_places[j]), simplicity_score)

                S = S_before_change
                print('S =',S)

        swap(best_result[0][0], best_result[0][1])
        swaps.append(best_result[0])
        print('#',S)
        print()
        S = Simplify(S)
        print()
    print(len(swaps))
    print(swaps)

