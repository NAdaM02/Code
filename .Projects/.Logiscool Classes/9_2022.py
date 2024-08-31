myList = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def RemoveOdd(l):
    f = list(l)
    count = 0
    for i in range (len(l)):
        if(l[i] % 2 == 1):
            f.pop(i-count)
            count += 1
    return f
#print(RemoveOdd(myList))


def PrintInts():
    print(RemoveOdd(myList))
    for i in range(0,int(input('N: '))):
        print(i, end=' ')
#PrintInts


myMatrix = [[1,1,2,4,8],[16,32],[64,128,256,512,1024]]

def MatrixSum(m):
    sum = 0
    for row in m:
        for col in row:
            sum += col
    return sum
#print(MatrixSum(myMatrix))


my_list = [8,3,5,1,2,7,6,9,4]
def MergeSort(l):
    size = len(l)
    if (size > 1):
        middle = size // 2
        left_list = l[:middle]
        right_list = l[middle:]
        MergeSort(left_list)
        MergeSort(right_list)
        left_size = len(left_list)
        right_size = len(right_list)
        p = 0
        q = 0
        r = 0
        while (p < left_size and q < right_size):
            if (left_list[p] < right_list[p]):
                l[r] = left_list[p]
                p += 1
            else:
                l[r] = right_list[q]
                q += 1
            r += 1
        while (p < left_size):
            l[r] = left_list[p]
            p += 1
            r += 1
        while (q < right_size):
            l[r] = right_list[q]
            q += 1
            r += 1
    return l
print(MergeSort(my_list))


def DigitSum(n):
    sum = 0
    while (n > 0):
        last_digit = n % 10
        sum += last_digit
        n = (n-last_digit)/10
    return(int(sum))
print(DigitSum(int(input('Give me a number: '))))
