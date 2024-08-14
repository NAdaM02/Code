import random

board = [" "," 1"," 2"," 3","1 ","- ","- ","- ","2 ","- ","- ","- ","3 ","- ","- ","- "]
player1_turn = True
endgame = False
while endgame == False:
    for i in range(0,16,4):
        print(board[i] + board[i+1]+ board[i+2]+ board[i+3])
    if player1_turn:
        print("Az egyes játékos van soron.")
    else:
        print("A kettes játékos van soron.")
    new_place = False
    while new_place == False:
        row = 0
        col = 0
        while row < 1 or row > 3:
            row = int(input("Add meg a sort: "))
        while col < 1 or col > 3:
            col = int(input("Add meg az oszlopot: "))
        if board[4*row + col] == "- ":
            new_place = True
    if player1_turn:
        board[4*row + col] = "x "
    else:
        board[4*row + col] = "o "
    # nyert-e valaki
    if(board[5] == board[6] and board[6] == board[7] and board[5] != "- "):
        if player1_turn:
            print("Egyes játékos nyert, ügyi vagy!")
        else:
            print("Kettes játékos nyert, ügyi vagy!")
        endgame = True
    if endgame == False and "- " not in board:
        endgame = True
        print("Döntetlen")
    if endgame == False:
        if player1_turn:
            player1_turn = False
        else:
            player1_turn = True
