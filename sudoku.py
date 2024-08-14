from time import sleep as wait
import os
from time import perf_counter as now

#S O D U K U
def do(board=""):
    global p_count, start
    if ( board == "" ):
        board1 = [
                [' ',  ' ',  '6',    '5',  ' ',  ' ',    ' ',  ' ',  ' '],
                #
                ['7',  ' ',  '5',    ' ',  ' ',  '2',    '3',  ' ',  ' '],
                #
                [' ',  '3',  ' ',    ' ',  ' ',  ' ',    ' ',  '8',  ' '],
                #
                #
                [' ',  '5',  ' ',    ' ',  '9',  '6',    ' ',  '7',  ' '],
                #
                ['1',  ' ',  '4',    ' ',  ' ',  ' ',    ' ',  ' ',  '8'],
                #
                [' ',  ' ',  ' ',    '8',  '2',  ' ',    ' ',  ' ',  ' '],
                #
                #
                [' ',  '1',  ' ',    ' ',  ' ',  ' ',    ' ',  '9',  ' '],
                #
                [' ',  ' ',  '7',    '2',  ' ',  ' ',    '4',  ' ',  ' '],
                #
                [' ',  ' ',  ' ',    ' ',  ' ',  '7',    '5',  ' ',  ' ']
                ]
        
        board2 = [
                [' ',  '3',  '6',    '8',  '1',  '9',    '5',  ' ',  '2'],
                #
                ['9',  ' ',  '1',    '2',  '5',  ' ',    ' ',  '3',  ' '],
                #
                ['2',  ' ',  '5',    ' ',  '3',  '6',    '9',  ' ',  '1'],
                #
                #
                [' ',  '2',  ' ',    '9',  ' ',  ' ',    '1',  ' ',  ' '],
                #
                [' ',  ' ',  '3',    '1',  '8',  ' ',    '2',  '5',  '9'],
                #
                [' ',  '1',  '9',    ' ',  '2',  ' ',    ' ',  ' ',  ' '],
                #
                #
                ['1',  ' ',  '2',    ' ',  ' ',  '8',    '3',  '9',  '5'],
                #
                ['3',  '9',  ' ',    '5',  ' ',  '2',    ' ',  '1',  '8'],
                #
                [' ',  '5',  ' ',    '3',  '9',  '1',    '7',  '2',  ' ']
                ]
        
        board3 = [
                "2..5.74.6",
                "....31...",
                "......23.",
                "....2....",
                "86.31....",
                ".45......",
                "..9...7..",
                "..695...2",
                "..1..6..8"
        ]
        
        board4 = [
                "8....7.5.",
                "...1.....",
                "....5.6..",
                "5....1.2.",
                ".7..28...",
                "98....7..",
                "..9.....1",
                "....74..5",
                "7....5.93"
        ]

        board5 = '1.......4 5....3.7. .....2... ..6.4..18 ...8...3. 8.492...6 .19...... ..76...4. 4....9..1'
        
        board = board5

    if type(board) == type(""):
        board = list(map(lambda x: list(x.replace('.',' ')), board.split(' ')))
    elif type(board[0]) == type("") :
        board = list(map(lambda x: list(x.replace('.',' ')), board))

    def pBoard(bo):
        for i in range(len(bo)):
            if ( i % 3 == 0 and i != 0 ):
                print("- - - - - - - - - - - - -")
            for j in range(len(bo[0])):
                if ( j % 3 == 0 and j != 0 ):
                   print(" | ", end=" ")
                if ( j == 8 ):
                    print(bo[i][j])
                else:
                    print(str(bo[i][j]), end=" ")

    def findNull(bo):
        for i in range(0,9):
            for j in range(0,9):
                if (bo[i][j] == ' ' ):
                    return (i,j)
        return None

    def valid(bo, num, pos): #pos = [ sor, oszlop ]
        # sor
        for sor_elem in range(len(bo[0])):
            if ( bo[pos[0]][sor_elem] == num and pos[1] != sor_elem ):
                return False
        # oszlop
        for oszlop_elem in range(len(bo)):
            if ( bo[oszlop_elem][pos[1]] == num and pos[0] != oszlop_elem ):
                return False
        # negyzet
        boxX = pos[1] // 3
        boxY = pos[0] // 3
        for i in range(boxY *3, boxY*3+3):
            for j in range(boxX * 3, boxX * 3 + 3):
                if ( board[i][j] == num and (i,j) != pos ):
                    return False
        return True

    def solve(bo):
        global p_count, start
        find = findNull(bo)
        if not find:
            return True
        else:
            if now()-start > 30 and start != 0:
                return 69
            sor,oszlop = find

        for i in range(1,10):  #1,2,3...9
            if ( valid(bo,f'{i}',(sor,oszlop)) ):
                bo[sor][oszlop] = f'{i}'
                
                """if p_count % 10 == 0:
                    os.system('cls')
                    pBoard(bo)
                p_count += 1"""

                if (solve(bo)):
                    return True
                bo[sor][oszlop] = ' '
        return False

    os.system('cls')
    pBoard(board)
    print()
    input("Press enter to solve!")
    
    start = now()

    result = solve(board)

    if result != 69 :
        print("\n\n\n")
        print('Solution:')
        pBoard(board)

        print()
        print(f"Elapsed: {now()-start}s")
        print()
    else:
        print("Puzzle is probably incorrect.")

start = 0
p_count = 0

board_input = ""

print('Give board:\n')

for i in range(1,4):
    for j in range(1,4):
        board_input += (input().replace(' ','.') + " " if not(i==3 and j==3) else input().replace(' ','.'))
    print()


do(board_input)
