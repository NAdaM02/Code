num_of_roulettes,len_of_tags = input().split(' ')
num_of_roulettes,len_of_tags = int(num_of_roulettes),int(len_of_tags)
tags = []
for i in range(num_of_roulettes):
    tags.append(tuple(input()))
def is_it_similar(tag1,tag2):
    tag1,tag2 = list(tag1),list(tag2)
    results = []
    for n in range(len_of_tags):
        similar = True
        for i in range(len_of_tags):
            if(i+n >= len_of_tags):
                if(not(tag1[i]==tag2[i+n-len_of_tags])):
                    similar = False
                    break
            else:
                if (not(tag1[i] == tag2[i+n])):
                    similar = False
                    break
        results.append(similar)
    if(True in results):
        return True
    else:
        return False
sum = 0
for k in range(num_of_roulettes-1):
    for l in range(k+1,num_of_roulettes):
        possible = True
        for i in tags[k]:
            if(not(i in tags[l])):
                possible = False
                break
        if(possible):
            if(is_it_similar(tags[k],tags[l]) == True):
                sum += 1
print(sum)
