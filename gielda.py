import random
import remibank as rb
import os

class Aukcja:
    def __init__(self):
        self.current = None
        self.highest = 1
        self.winner = None

    def start(self):
        self.winner = None
        h = open("a.txt", 'r')
        slow = eval(h.read())
        h.close()
        t = list(slow.keys())
        dupa = list(slow.values())
        x = 1
        if 0 in dupa:
            while True:
                wylos = random.randint(0, len(slow.keys()) - 1)
                x = slow[t[wylos]]
                if x == 0:
                    break
            self.current = t[wylos]
            self.highest = round(rb.stat() / 50, 2)
            b = 'obr/' + self.current + '.png'
            return f'Dzisiejsza aukcja: {self.current}, cena: {self.highest} REMICOIN', b
        else:
            return f'Nie ma diewczynek na aukcje!', None

    def bid(self, price, uzyt):
        price = round(price, 2)
        u = rb.User(uzyt)
        if price <= u.cstan():
            if self.current != None:
                if price > self.highest:
                    self.highest = price
                    self.winner = uzyt
                    return f'<@!{self.winner}> wygra dając {self.highest} remizetonow!'
                else:
                    return f'Musisz dac wiecej niz {self.highest}!'
            else: f'Nie ma nic na aukcji'
        else:
            return f'Nie masz tyle pieniedzy!'

    def end(self):
        h = open("a.txt", 'r')
        slow = eval(h.read())
        h.close()
        if self.winner != None:
            slow[self.current] = self.winner
            x = self.current
            p = self.highest
            h = open("a.txt", 'w')
            h.write(str(slow))
            h.close()
            u = rb.User(self.winner)
            u.zabierz(self.highest)
            self.current = None
            self.highest = 0
            self.winner = None
            return f'Aukcje wygrywa <@!{slow[x]}>! {x} sprzedana za {p}'

        else:
            return f'Nikt nie chcial {self.current}'

    def sprawdz(self, post):
        h = open("a.txt", 'r')
        slow = eval(h.read())
        h.close()
        x = slow[post]
        if x != 0:
            return f'{post} nalezy do <@!{x}>'
        else:
            return f'Nikt nie ma {post}'

    def lista(self, us):
        h = open("a.txt", 'r')
        slow = eval(h.read())
        h.close()
        x = [k for k, v in slow.items() if v == str(us)]
        if x != None:
            return f'Masz: {x}'
        else:
            return f'Nie masz nic'


    def zwrot(self):
        if self.current == None:
            x = 'Nic'
        else:
            x = self.current

        return f'Aukcja: {x} za {self.highest}'


def sprzedaj(sp, kp, wafu, cena):
    cena = float(cena)
    s = rb.User(sp)
    k = rb.User(kp)
    h = open("a.txt", 'r')
    slow = eval(h.read())
    h.close()
    x = [k for k, v in slow.items() if v == str(sp)]
    if wafu in x:
        if k.cstan() < cena:
            return f'Masz za mało RMC biedaku'
        elif cena < 1:
            return f'Cena musi być większa niż 1!'
        else:
            s.zabierz(-cena)
            k.zabierz(cena)

            slow[wafu] = kp

            h = open("a.txt", 'w')
            h.write(str(slow))
            h.close()





            return f'Kupujesz: {wafu}, stan sprzedajacego wynosi {s.cstan()}, stan kupujacego wynosi {k.cstan()}'
    else:
        return f'Nie masz tego!'




class Faktoro:

    def __init__(self, name):
        self.name = str(name)

    def cena(self, b, poziom):
        f = open('conf/ceny.txt', 'r')
        x = eval(f.read())
        f.close()
        cen = x[b]
        poziom = ((poziom + 1)*1.1)
        wyn = round(((round((rb.stat() / 50)*cen, 2) * poziom)/5),2)
        return wyn

    def scen(self, bud):
        nazwa = self.name
        plik = "bank/bud/" + nazwa + ".txt"
        f = open('conf/bud.txt', 'r')
        slow = eval(f.read())
        f.close()

        if not os.path.isfile(plik):
            f = open(plik, 'w')
            f.write(str(slow))
            f.close()
            return f'Inicjalizacja'
        else:
            k = rb.User(nazwa)
            f = open(plik, 'r')
            posiadane = eval(f.read())
            f.close()
            poziom = int(posiadane[bud])
            cen = self.cena(bud, poziom)
            return f'Kolejny poziom {bud} kosztuje {cen} RMC'

    def budynki(self):
        nazwa = self.name
        plik = "bank/bud/" + nazwa + ".txt"
        f = open('conf/bud.txt', 'r')
        slow = eval(f.read())
        f.close()

        if not os.path.isfile(plik):
            f = open(plik, 'w')
            f.write(str(slow))
            f.close()
            return f'Inicjalizacja'
        else:
            s = f'Twoje budynki:\n'
            f = open(plik, 'r')
            posiadane = eval(f.read())
            f.close()
            for x in posiadane.keys():
                s = s + f'{x} poziomu {posiadane[x]}\n '
            return s


    def upgrade(self, bud):
        nazwa = self.name
        plik = "bank/bud/" + nazwa + ".txt"
        f = open('conf/bud.txt', 'r')
        slow = eval(f.read())
        f.close()

        if not os.path.isfile(plik):
            f = open(plik, 'w')
            f.write(str(slow))
            f.close()
            return f'Inicjalizacja'
        else:
            k = rb.User(nazwa)
            f = open(plik, 'r')
            posiadane = eval(f.read())
            f.close()
            poziom = int(posiadane[bud])
            cen = self.cena(bud, poziom)
            if k.cstan() < cen:
                return f'Masz za mało RMC biedaku'
            else:

                k.zabierz(cen)
                np = poziom + 1
                posiadane[bud] = np

                h = open(plik, 'w')
                h.write(str(posiadane))
                h.close()

                return f'Poziom {bud} wynosi {np}'


def update():
    f = open('conf/doc.txt', 'r')
    slow = eval(f.read())
    f.close()
    dire = f'bank/bud/'
    pliki = os.listdir(dire)
    for x in pliki:
        stan = 0
        try:
            f = open(dire + x, 'r')
            p = eval(f.read())
            f.close()
            for y in p.keys():
                poz = int(p[y])
                stan = stan + round(int(slow[y])*poz*1.2, 2)
            dupa = x[:-4]
            u = rb.User(dupa)
            zmienna = u.dodaj(stan)

        except:
            pass
    return f'Zaktualizowano dochody'


def spraw(user):
    f = open('conf/doc.txt', 'r')
    slow = eval(f.read())
    f.close()
    dire = f'bank/bud/{user}.txt'
    stan = 0
    try:
        f = open(dire, 'r')
        p = eval(f.read())
        f.close()
        for y in p.keys():
            poz = int(p[y])
            stan = stan + round(int(slow[y]) * poz * 1.2, 2)
        dupa = x[:-4]
    except:
        pass
    return f'Zarabiasz {stan} RMC'