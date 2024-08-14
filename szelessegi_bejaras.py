my_matrix = [[0,1,1,0,0,1],[1,0,1,1,0,0],[1,1,0,1,0,1],[0,1,1,0,1,0],[0,0,0,1,0,1],[1,0,1,0,1,0]]
start_x = 0
start_y = 0
start = (start_y, start_x)
places = []

def SzelessegiBejaras(matrix,start):
    helper = matrix
    s_x = start[0]
    s_y = start[1]
    for x in range(s_x-1,s_x+3):
        for y in range(s_y-1,s_y+3):
            if (x >= 0 and y >= 0 and x < len(helper) and y < len(helper) and helper[x][y] == 1):
                places.append((x,y))
                helper[x][y] = 0
                SzelessegiBejaras(helper,(x,y))
    return places

places = SzelessegiBejaras(my_matrix,start)
print(places)
for y in range(len(my_matrix)):
    for x in range(len(my_matrix[0])):
        is_it_it = False
        for coords in places:
            if (coords[0] == x and coords[1] == y):
                is_it_it = True
        if (is_it_it):
            print(1, end=' ')
        else:
            print(0, end=' ')
    print('')

