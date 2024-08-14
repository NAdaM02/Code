draw = open('drawFile.txt', 'w+')
for i in range(10):
    j = 0
    while (j < 10):
        for k in range(j):
            draw.write('-')
        draw.write('  ')
        for k in range(10 - j):
            draw.write('-')
        draw.write('\n')
        j+=1
    while (j > 0):
        for k in range(j):
            draw.write('-')
        draw.write('  ')
        for k in range(10 - j):
            draw.write('-')
        draw.write('\n')
        j-=1
draw.seek(0)
print(draw.read())
draw.close()
