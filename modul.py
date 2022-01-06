import random
import os
import pvp
import level as lvl
import asyncio

h = open("conf/list.txt", 'r')
stringi = h.read()
t = stringi.split()
h.close()


class User:

    def __init__(self, name):
        self.name = name

    def poziom(self):
        plik = 'baza/' + self.name + '.txt'
        if os.path.isfile(plik):
            f = open(plik, 'r')
            slow = eval(f.read())
            f.close()
            xp = 0
            for x in slow.keys():
                xp = xp + slow[x]
            xpr = xp
            poziom = 1
            while xpr > 0:
                poziom = 1 + poziom
                xpr = int(xpr - 100 * poziom)
            return f'Poziom <@!{self.name}>: {poziom}', poziom
        else:
            return f'Poziom <@!{self.name}>: 0'

    def read(self):
        nazwa = str(self.name)
        plik = "baza/" + nazwa + ".txt"
        filesize = os.path.getsize(plik)
        f = open(plik, 'r')
        if filesize == 0:
            f.close()
            return f'Nie posiadasz jeszcze nic, użyj komedy %los!'
        else:
            slow = eval(f.read())
            pz = {}
            ex = f''
            ik = 0
            for x in sorted(slow.keys(), reverse=True):
                post = lvl.Postac(x, slow[x])
                off = ik + post.lvl()
                pz[off] = (x, slow[x])
                ik = ik + 0.001
            f.close()
            for u in sorted(pz, reverse=True):
                ex = ex + f'{pz[u][0]}: xp: {pz[u][1]} poziom: {int(u)}\n'
            return ex

    def pok(self, co):
        obraz = co
        nazwa = str(self.name)
        plik = "baza/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            return f'Nie posiadasz jeszcze nic, użyj komedy %los!', 'nic'
        else:
            f = open(plik, "r")
            slow = eval(f.read())
            if obraz in slow.keys():
                post = lvl.Postac(obraz, slow[obraz])
                f.close()
                try:
                    atk_pos, atk_neg, df_pos, df_neg, krt, hp, sp = pvp.staty(obraz,nazwa)
                except: atk_pos, atk_neg, df_pos, df_neg, krt, hp, sp = 0, 0, 0, 0, 0, 0, 0
                return f'Twoja {obraz}, jej poziom to: {post.lvl()}\n Atak pozytywny:{atk_pos} Atak negatywny:{atk_neg} Obrona pozytywna:{df_pos} Obrona negatywna:{df_neg} Szansa na cios krytyczny:{krt}% HP: {hp} Szybkość: {sp}', obraz
            else:
                f.close()
                return f'Nie posiadasz jeszcze tego!', 'nic'

    def los(self):
        wylos = random.randint(0, len(t))
        nazwa = str(self.name)
        plik = "baza/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            slow = {}
        else:
            f = open(plik, 'r')
            slow = eval(f.read())
            f.close()
        if t[wylos] in slow.keys():
            xp = slow[t[wylos]]
            slow[t[wylos]] = xp + 100
            f = open(plik, "w")
            f.write(str(slow))
            f.close()
            return f'Juz posiadasz {t[wylos]} dodano do niej 100xp!', t[wylos]
        else:
            slow.update({t[wylos]: 0})
            f = open(plik, "w")
            f.write(str(slow))
            f.close()
            return f'Brawo wylosowales {t[wylos]}!', t[wylos]

    async def quest(self, postac):
        nazwa = str(self.name)
        plik = "baza/" + nazwa + ".txt"
        status = 'n'
        postac = str(postac)
        if not os.path.isfile(plik):
            return f'Nie posiadasz jeszcze nic, użyj komedy %los!', status, 0, 0
        elif postac == 'all':
            f = open(plik, "r")
            slow = eval(f.read())
            f.close()
            ex = f''
            for x in slow.keys():
                try:
                    f = open('baza/licznik/'+ nazwa + '/' + x + '.txt')
                    stat = str(f.read())
                    f.close()
                    if stat != '0':
                        ex = ex + f'{x} jest na misji wroci za: {stat} sekund\n'
                except: pass
            return ex, status, 0, 0

        else:
            f = open(plik, "r")
            slow = eval(f.read())
            if postac in slow.keys():
                post = lvl.Postac(postac, slow[postac])
                f.close()
                nazwac = "baza/licznik/" + nazwa + '/' + postac + '.txt'
                if not os.path.isdir("baza/licznik/" + nazwa):
                    os.mkdir("baza/licznik/" + nazwa)
                    f = open("baza/licznik/" + nazwa + '/' + "status.txt", 'w')
                    f.write('0')
                    f.close()
                    return f'Zainicjalizowano baze danych dla uzytkownika uzyj komendy jeszcze raz!', status, 0, 0
                else:
                    if not os.path.isfile(nazwac):
                        f = open(nazwac, "w")
                        f.write('0')
                        f.close()
                        return f'Dodano postac uzyj komendy jeszcze raz!', status, 0, 0
                    else:
                        f = open(nazwac, "r")
                        tajm = f.read()
                        f.close()
                        if int(tajm) > 0:
                            return f'Twoja {postac} jest na misji wroci za {tajm} sekund', status, 0, 0
                        else:
                            f = open("baza/licznik/" + nazwa + '/' + "status.txt", 'r')
                            ilosc = int(f.read())
                            f.close()
                            plikjakis = 'baza/' + nazwa + '.txt'
                            f = open(plikjakis, 'r')
                            slownik = eval(f.read())
                            f.close()
                            xp = 0
                            for x in slownik.keys():
                                xp = xp + slownik[x]
                            xpr = xp
                            poziom = 1
                            while xpr > 0:
                                poziom = 1 + poziom
                                xpr = int(xpr - 100 * poziom)
                            poziom = int(poziom/25) + 2
                            if ilosc >= poziom:
                                return f'Osiagnieto maksymalna ilosc zadan: {poziom}!', status, 0, 0
                            else:
                                kwesty = []
                                nagrody = []
                                czasy = []
                                for poz in range(3):
                                    op, nag, cza = post.quest()
                                    czasy.append(cza)
                                    nagrody.append(nag)
                                    jajo = poz + 1
                                    czass =int((float(cza/60) - int(cza/60))*60)
                                    kwesty.append(f'{jajo}. {op}Nagroda xp: {nag}, czas: {int(cza/60)}:{czass}\n')
                                strong = "Wybierz zadanie masz 12 sekund (%wybierz (numer zadania)):\n"
                                for i in range(len(kwesty)):
                                    strong = strong + kwesty[i]
                                status = 'y'
                                return strong, status, czasy, nagrody

            else:
                f.close()
                return f'Nie posiadasz jeszcze tego!', status, 0, 0

    async def zacznij(self, xp, czas, postac):
        nazwa = str(self.name)
        plik = "baza/" + nazwa + ".txt"
        f = open(plik, "r")
        slow = eval(f.read())
        f.close()
        post = lvl.Postac(postac, slow[postac])
        xpp = xp + slow[postac]
        slow[postac] = xpp
        f = open(plik, "w")
        f.write(str(slow))
        f.close()
        await post.licznik(czas, nazwa)
        return

    def ustaw(self, postac):
        nazwa = str(self.name)
        plik = 'baza/main/' + nazwa + '.txt'
        plikc = 'baza/' + nazwa + '.txt'
        f = open(plikc, 'r')
        slow = eval(f.read())
        f.close()
        if postac in slow.keys():
            f = open(plik, 'w')
            f.write(str(postac))
            f.close()
            return f'Ustawiono {postac} jako glowna!'
        else:
            return f'Nie masz takiej postaci!'


def topkon():
    basepath = 'baza/'
    e = []
    lista = {}
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            e.append(entry)
    for x in e:
        t = x.replace('.txt', '')
        us = User(t)
        niezmienna, p = us.poziom()
        lista[p] = t
    return lista

def topdziew():
    basepath = 'baza/'
    e = []
    lista = {}
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            e.append(entry)
    dlug = len(t)
    for i in range(0, dlug):
        post = t[i]
        xp = 0
        for x in e:
            f = open('baza/' + x, 'r')
            slow = eval(f.read())
            f.close()
            if post in slow.keys():
                xp = xp + slow[post]
        lista[post] = xp
    lista = {value: key for (key, value) in lista.items()}
    wyn = f'Najlepsze dziewczynki: \n'
    for x in sorted(lista.keys(), reverse=True):
        dz = lvl.Postac(lista[x], x)
        poz = dz.lvl()
        wyn = wyn + f'{lista[x]}: {x} xp, serwerowy poziom: {poz}\n'
    return wyn
