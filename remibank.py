import os
import matplotlib.pyplot as plt
import datetime

class User:
    def __init__(self, name):
        self.name = name

    def zaloz(self):
        nazwa = self.name
        plik = "bank/" + nazwa + ".txt"
        nic = '0'
        if not os.path.isfile(plik):
            f = open(plik, 'w')
            f.write(nic)
            f.close()
            return f'Pomyslnie zalozono konto'
        else:
            return f'Posiadasz juz konto!'

    def dodaj(self, ilosc):
        ilosc = float(ilosc)
        nazwa = str(self.name)
        plik = "bank/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            return f'Nie znaleziono takiego konta'
        else:
            f = open(plik, 'r')
            stan = float(f.read())
            f.close()
            stapo = stan + ilosc
            stapo = str(stapo)
            f = open(plik, 'w')
            f.write(stapo)
            f.close()
            return f'Dodano {ilosc} RemiZetonow! Twoj stan konta wynosi {stapo}!'

    def zabierz(self, ilosc):
        nazwa = str(self.name)
        plik = "bank/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            return None
        else:
            f = open(plik, 'r')
            stan = float(f.read())
            f.close()
            stapo = stan - ilosc
            stapo = str(stapo)
            f = open(plik, 'w')
            f.write(stapo)
            f.close()
            return None

    def stan(self):
        nazwa = self.name
        plik = "bank/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            return f'Nie znaleziono takiego konta'
        else:
            f = open(plik, 'r')
            stan = f.read()
            f.close()
            return f'Twoj stan konta wynosi {stan} RemiZetonow!'

    def cstan(self):
        nazwa = self.name
        plik = "bank/" + nazwa + ".txt"
        if not os.path.isfile(plik):
            return 0
        else:
            f = open(plik, 'r')
            stan = f.read()
            f.close()
            return float(stan)

    def przelew(self, user2, ilosc):
        nazwa = self.name
        try:
            ilosc = float(ilosc)
        except:
            return f'Ilosc musi byc liczba calkowita!'
        plik = "bank/" + nazwa + ".txt"
        plik2 = "bank/" + user2 + ".txt"
        if not os.path.isfile(plik):
            return f'Nie posiadasz konta'
        elif not os.path.isfile(plik2):
            return f'Adresat nie posiada konta!'
        else:
            f = open(plik, 'r')
            stan1 = float(f.read())
            f.close()
            f = open(plik2, 'r')
            stan2 = float(f.read())
            f.close()
            if ilosc <= 0:
                return f'Nie mozna krasc debilu'
            elif ilosc > stan1:
                return f'Nie masz tyle RemiZetonow!'
            else:
                postan1 = stan1 - ilosc
                postan2 = stan2 + ilosc
                postan1 = str(postan1)
                postan2 = str(postan2)
                f = open(plik, 'w')
                f.write(postan1)
                f.close()
                f = open(plik2, 'w')
                f.write(postan2)
                f.close()
                return f'Sukcesywnie przelano {ilosc} RemiZetonow! Twoj stan: {postan1}. Stan odbiorcy: {postan2}'


def div(n, d):
    return n / d if d else 0

def update(dzis):
    plik = 'bank/stat/stat.txt'
    f = open(plik, 'r')
    lista = eval(f.read())
    f.close()
    lista.insert(0, dzis)
    lista.pop()
    f = open(plik, 'w')
    f.write(str(lista))
    f.close()




def stat():
    stan = 0
    dire = 'bank/'
    pliki = os.listdir(dire)
    for x in pliki:
        try:
            f = open(dire + x, 'r')
            stan = stan + float(f.read())
            f.close()
        except: pass

    return stan

def plot():
    dni = []
    now = datetime.date.today()
    dzien = datetime.timedelta(1)
    for i in range(0, 31):
        x = now - dzien*i
        y = f'{x.month}.{x.day}'
        dni.append(y)
    dni.reverse()


    plik = 'bank/stat/stat.txt'
    f = open(plik, 'r')
    lista = eval(f.read())
    lista.reverse()
    f.close()
    infla = []

    for i in range(1, len(lista)):
        wsp = -((div(int(lista[i-1]), int(lista[i])) - 1) * 100)
        infla.append(wsp)

    fig, axs = plt.subplots(1, 2, figsize=(9, 3))
    axs[0].plot(dni, lista)
    axs[0].set_title('Ilosc REMICOIN w obiegu')
    axs[0].xaxis.set_tick_params(rotation=45, labelsize=7)
    dni.pop(0)
    axs[1].plot(dni, infla)
    axs[1].set_title('Inflacja w %')
    axs[1].xaxis.set_tick_params(rotation=45, labelsize=7)

    plt.savefig('bank/stat/fumo.png')

    inflacja = -((div(int(lista[0]), int(lista[-1])) - 1) * 100)
    return f'Ilosc REMICOIN: {stat()}\nInflacja: {round(infla[-1],3)}% dzisiaj, {round(inflacja,3)}% w tym miesiacu'
