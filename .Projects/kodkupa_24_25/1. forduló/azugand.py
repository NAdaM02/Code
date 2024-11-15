csucsok_szama, lekerdezesek_szama = input().split() # N, Q
csucsok_szama, lekerdezesek_szama = int(csucsok_szama), int(lekerdezesek_szama)

csucs_ertekek = tuple(map(int, input().split())) # V0, V1, . . . , VN

irany_konyvtar = [[] for i in range(csucsok_szama)]
iranyok_tesztelve = [False for i in range(csucsok_szama)]

import numpy
def ut_a_celig(elozo_csucsok, jelenlegi_csucs, cel_csucs):
    elozo_csucsok.append(jelenlegi_csucs)
    if jelenlegi_csucs == cel_csucs:
        return elozo_csucsok

    if not iranyok_tesztelve[jelenlegi_csucs]:
        for i in range(csucsok_szama):
            if i != jelenlegi_csucs:
                if numpy.bitwise_and(csucs_ertekek[i], csucs_ertekek[jelenlegi_csucs]) != 0:
                    if i not in irany_konyvtar[jelenlegi_csucs]:
                        irany_konyvtar[jelenlegi_csucs].append(i)
                    if i == cel_csucs:
                        return elozo_csucsok + [cel_csucs]
        iranyok_tesztelve[jelenlegi_csucs] = True
    
    for lehetseges_uj_csucs in irany_konyvtar[jelenlegi_csucs]:
        if lehetseges_uj_csucs not in elozo_csucsok:
            ut_a_celig(elozo_csucsok, lehetseges_uj_csucs, cel_csucs)

valaszok = []
for lekerdezes_sorszama in range(lekerdezesek_szama):
    indulas_csucs, cel_csucs = input().split()
    indulas_csucs, cel_csucs = int(indulas_csucs)-1, int(cel_csucs)-1

    bejart_csucsok = ut_a_celig([], indulas_csucs, cel_csucs)
    if bejart_csucsok != None:
        valaszok.append(f"{bejart_csucsok} {len(bejart_csucsok)-1}")
    else:
        valaszok.append(-1)
    #valaszok.append(len(bejart_csucsok)-1)

for valasz in valaszok: print(valasz)
