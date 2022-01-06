import random
import level as lvl
import asyncio
import os

def get(user1, user2):
    f = open('baza/main/' + user1 + '.txt')
    postac1 = f.read()
    f.close()
    f = open('baza/main/' + user2 + '.txt')
    postac2 = f.read()
    f.close()
    return postac1, postac2

def staty(postac,user):
    f_1 = open('conf/staty.txt')
    lista = eval(f_1.read())
    f_1.close()

    #uzyt = str(self.user)
    f = open('baza/' + user + '.txt', 'r')
    slow = eval(f.read())                
    f.close()
    pos = lvl.Postac(postac, slow[postac])
    poziom = int(pos.lvl())

    staty = lista[postac]
    atk_pos = int(staty['atk_pos'])
    atk_pos += int(round(atk_pos*(poziom/20)))
    atk_neg = int(staty['atk_neg'])
    atk_neg += int(round(atk_neg*(poziom/20)))
    df_pos = int(staty['df_pos'])
    df_pos += int(round(df_pos*(poziom/20)))
    df_neg = int(staty['df_neg'])
    df_neg += int(round(df_neg*(poziom/20)))
    kryt = int(staty['kryt'])
    hp = int(staty['hp'])
    hp += int(round(hp*(poziom/20)))
    sp = int(staty['sp'])
    sp += int(round(sp*((poziom)/400)))
    return atk_pos, atk_neg, df_pos, df_neg, kryt, hp, sp


class Pvp:
    def __init__(self, user1, user2):
        self.user1 = user1
        self.user2 = user2

    def atak(self, post1, post2):
        atk_pos_1, atk_neg_1, def_pos_1, def_neg_1, kryt_1, hp_1, sp_1 = staty(post1,self.user1)
        atk_pos_2, atk_neg_2, def_pos_2, def_neg_2, kryt_2, hp_2, sp_2 = staty(post2,self.user2)
        k_1 = 1 - kryt_1/100
        k_2 = 1 - kryt_2/100
        gb_1 = 0
        gb_2 = 0
        log = f''
        while True:
            gb_1+=sp_1
            gb_2+=sp_2
            crit=1
            if gb_1>=gb_2:
                gb_1-=sp_1
                if random.uniform(0, 1) > k_1:
                    crit = 2
                    log += f'Krytyk! '
                obr_1 = ((atk_neg_1*crit-def_neg_2)+(atk_neg_1*crit-def_neg_2))
                if obr_1 <= 0:
                    obr_1 = 1
                hp_2 -= obr_1
                if hp_2 <= 0:
                    hp_2 = 0
                log += f'{post1} atakuje {post2} za {obr_1}. HP {post2}: {hp_2}\n'
                if hp_2 == 0:
                    uzyt = str(self.user1)
                    fil = open('baza/' + uzyt + '.txt', 'r')
                    slow = eval(fil.read())
                    fil.close()
                    pos = lvl.Postac(post1, slow[post1])
                    lewel = int(pos.lvl())

                    xp = 100 + 50*int(lewel**1.1)
                    xpp = xp + slow[post1]
                    slow[post1] = xpp
                    fil = open('baza/' + self.user1 + '.txt', "w")
                    fil.write(str(slow))
                    fil.close()
                    log += f'{post1} <@!{self.user1}> wygrywa z {hp_1} hp! Otrzymala {xp} xp'
                    break
            else:
                gb_2-=sp_2
                if random.uniform(0, 1) > k_2:
                    crit = 2
                    log = log +f'Krytyk! '
                obr_2 = ((atk_neg_2*crit-def_neg_1)+(atk_neg_2*crit-def_neg_1))
                if obr_2 <= 0:
                    obr_2 = 1
                hp_1 = hp_1 - obr_2
                if hp_1 <= 0:
                    hp_1 = 0
                log += f'{post2} atakuje {post1} za {obr_2}. HP {post1}: {hp_1}\n'
                if hp_1 == 0:
                    fil = open('baza/' + self.user2 + '.txt', 'r')
                    slow = eval(fil.read())
                    fil.close()
                    pos = lvl.Postac(post2, slow[post2])
                    lewel = int(pos.lvl())
                    xp = 100 + 50*int(lewel**1.1)
                    xpp = xp + slow[post2]
                    slow[post2] = xpp
                    fil = open('baza/' + self.user2 + '.txt', "w")
                    fil.write(str(slow))
                    fil.close()
                    log += f'{post2} <@!{self.user2}> wygrywa z {hp_2} hp! Otrzymala {xp} xp'
                    break
        return log
