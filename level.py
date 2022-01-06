import random
import asyncio
import os


class Postac:
    def __init__(self, name, xp):
        self.name = name
        self.xp = xp

    def lvl(self):
        xpr = self.xp
        poziom = 1
        while xpr > 0:
            poziom = 1 + poziom
            xpr = int(xpr - 100*poziom)
        return poziom

    def quest(self):
        poziom = self.lvl()
        lista = []
        h = open("conf/quest.txt", 'r')
        for x in h:
            lista.append(x)
        wyl = random.randint(0, len(lista))
        opis = lista[wyl]
        nagr = int(poziom*100*random.uniform(0.7, 1.5))
        cza = 100+int(poziom*25*random.uniform(0.6, 1.7))
        return opis, nagr, cza

    async def licznik(self, czas, uzyt):
        uzyt = str(uzyt)
        f = open("baza/licznik/" + uzyt + '/' + "status.txt", 'r')
        t = int(f.read())
        f.close()
        t = t + 1
        f = open("baza/licznik/" + uzyt + '/' + "status.txt", 'w')
        f.write(str(t))
        f.close()
        postac = str(self.name)
        plik = 'baza/licznik/' + uzyt + "/" + postac + '.txt'
        f = open(plik, 'r')
        f.close()
        x = czas
        while x > 0:
            await asyncio.sleep(1)
            x = x - 1
            tajm = x
            f = open(plik, "w")
            f.write(str(tajm))
            f.close()
        f = open("baza/licznik/" + uzyt + '/' + "status.txt", 'r')
        t = int(f.read())
        f.close()
        t = t - 1
        f = open("baza/licznik/" + uzyt + '/' + "status.txt", 'w')
        f.write(str(t))
        f.close()
        return
