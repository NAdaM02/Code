import pandas

def getcontent(filename):
    f = open(str(filename), "r", encoding="utf-8")
    lines = f.readlines()
    szamlatetel_adatok_sor = []
    for i in range(len(lines)):
        if("Számlatétel adatok" in lines[i]):
            szamlatetel_adatok_sor.append(i)

    reszek = []
    adatok = []

    for szam in szamlatetel_adatok_sor:
        reszek = []
        f = open("szo.txt", "w", encoding="utf-8")
        f.write("")
        f.close()
        for i in range(0,3):
            for j in lines[szam+2+i*3]:
                if(not(j==";")):
                    if(not(j=="\n")):
                        f = open("szo.txt", "a", encoding="utf-8")
                        f.write(j)
                        f.close()
                else:
                    f = open("szo.txt", "r", encoding="utf-8")
                    content = f.read()
                    try:
                        content = int(content)
                    except:
                        try:
                            content = float(content.replace(',', '.'))
                        except:
                            pass
                    reszek.append(content)
                    f.close()
                    f = open("szo.txt", "w", encoding="utf-8")
                    f.write("")
                    f.close()
        adatok.append(reszek)
    f.close()
    return adatok
my_list = getcontent("56675618_5120220002024496_10773381_HU.csv")
sum = 0
for i in my_list:
    for j in i:
        try:
            sum += j
        except:
            pass
print(my_list)
print(f'The sum of the purchases was: {int(sum/370.55)}$')
