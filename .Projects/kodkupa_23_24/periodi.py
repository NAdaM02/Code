N = int(input())
if  N == 0 :
    # example
    N = 14
    string = 'abacbaabcabccc'
    number_of_sections = 5
    sections = [[0, 13],[0, 3],[6, 11],[11, 13],[6, 10]]
else:
    string = input()
    number_of_sections = int(input())
    sections = []
    for i in range(number_of_sections):
        sections.append(list(map(int, input().split())))

for section_number in range(number_of_sections):
    sect = string[ sections[section_number][0] : sections[section_number][1]+1 ]
    can = False
    for i in range(1,int(len(sect)/2)+1):
        if len(sect)/i == int(len(sect)/i) :
            if (int(len(sect)/i)) * sect[0:i] == sect :
                can = True
    if can :
        print('YES')
    else:
        print('NO')
