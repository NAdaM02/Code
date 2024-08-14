input('Press enter to start process')

count_to = 10e6*2
count_to = int(count_to)
parts = 10
done_indicator = '¸'  # *._¸´˙`˛°˘^ˇ~
space_indicator = '_'

last = -1
for i in range(count_to):
    progress = int(i // (count_to/parts)) + 1
    if not last == progress:
        last = progress
        if not progress == parts:
            print('\r', (done_indicator + ' '*(len(space_indicator)-len(done_indicator)))*progress, space_indicator*((parts-progress)*len(done_indicator)), ' (', progress, '/', parts, ')', end='', sep='')
else:
    print('\r', (done_indicator+' '*(len(space_indicator)-len(done_indicator)))*parts, ' (', parts, '/', parts, ')', sep='')
    print('P r o c e s s   F i n i s h e d\n')
