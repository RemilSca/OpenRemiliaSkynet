import discord
import modul as mod
from discord.ext import commands
import random
import asyncio
import datetime
import os
import shutil
import pvp
import kaganiec as kg
from gpiozero import CPUTemperature
import gadugadu as gg
import remibank as rb
import nka
import gielda as gd
import numpy as np

remilia = open('token.txt', 'r')
token = remilia.read()
remilia.close()

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='%', intents=intents)

tajm = 5
tablica = []
a = []
stan = False
aukcja = gd.Aukcja()

async def daily():
    global stan
    global aukcja
    stan = True
    while True:
        gensokyo = bot.get_guild(647798243207544842)
        await asyncio.sleep(59)
        dzien = datetime.date.today()
        dzieni = dzien.weekday()
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        dzionek = datetime.datetime.now()
        koniec = dzionek.strftime("%Y-%m-%d:%H:%M")

        f = open('kaganiec/list.txt', 'r')
        plik = f.read()
        f.close()
        tablica = eval(plik)
        for x in tablica:
            a = x.split('=')
            if a[1] == koniec:
                kg.zdejmij(a[0])
                uzyt = int(a[0])
                user = gensokyo.get_member(uzyt)
                role = gensokyo.get_role(679786116110745600)
                await user.remove_roles(role)

        if dzieni == 4:
            if current_time == '09:00':
                channel = bot.get_channel(647798243714924569)
                await channel.send(
                    'https://cdn.discordapp.com/attachments/740344570310688899/814924929111294002/ff2.mp4')

        if current_time == '00:00':
            h = open("conf/list.txt", 'r')
            stringi = h.read()
            t = stringi.split()
            h.close()
            wylos = random.randint(0, len(t)-1)
            post = t[wylos]
            b = 'obr/' + post + '.png'
            channel = bot.get_channel(790562786992193548)
            await channel.send(f'Dzisiejsza dziewczynka (wedlug remila) jest: {post}!', file=discord.File(b))
            await channel.send(f'Zaktualizowano gielde')
            rb.update(rb.stat())

        if current_time == '12:01':
            channel = bot.get_channel(647798243714924569)
            x, b = aukcja.start()
            x = x + ' ' + gd.update()
            await channel.send(x, file=discord.File(b))

        if current_time == '22:00':
            channel = bot.get_channel(647798243714924569)
            x = aukcja.end()
            await channel.send(x)

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    global stan
    if stan==False:
        await daily()



@bot.event
async def on_command_error(ctx, exc):
    if isinstance(exc, commands.CommandOnCooldown):
        cza = int(exc.retry_after)
        czass = int((float(cza / 60) - int(cza / 60)) * 60)
        await ctx.channel.send(f'Sproboj za {int(cza / 60)}:{czass}')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.listen('on_message')
async def ai(message):
    usr = message.author.id
    msg = message.content
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    if message.author == bot.user:
        return
    elif msg.startswith('remi'):
        zaw = msg.replace('remi', '', 1)
        if len(zaw) > 2:
            x = gg.wiad(zaw)
            await message.channel.send(f'<@{usr}> {x}')
            



@bot.command(help='dodaje zakazane slowo')
@commands.has_role('MODE BANUJ')
async def zakaz(ctx, msg):
    t = []
    await asyncio.sleep(2)
    f = open('conf/ban.txt', 'r')
    t = eval(f.read())
    f.close()
    t.append(msg)
    t = str(t)
    f = open('conf/ban.txt', 'w')
    f.write(t)
    f.close()
    await ctx.channel.send(f"Dodano '{msg}'")


@bot.command(help='Usuwa zakazane slowo')
@commands.has_role('MODE BANUJ')
async def delzakaz(ctx, msg):
    t = []
    await asyncio.sleep(2)
    f = open('conf/ban.txt', 'r')
    t = eval(f.read())
    f.close()
    if msg in t:
        t.remove(msg)
    t = str(t)
    f = open('conf/ban.txt', 'w')
    f.write(t)
    f.close()
    await ctx.channel.send(f"Usunieto '{msg}'")


@bot.command(help='seks')
@commands.cooldown(1, 3600, commands.BucketType.guild)
async def sekssama(ctx, nick):
  gensokyo = bot.get_guild(647798243207544842)
  sakasama = gensokyo.get_member(273963808454606848)
  newnick = nick + 'sama'
  if len(nick) <= 28:
    await sakasama.edit(nick=newnick)
    await ctx.send(f'PepeLaugh-> {newnick} <-PepeLaugh ')
  else:
    await ctx.send(f'{newnick} jest niepoprawny Sadge ')



@bot.command(help='losuje postac do doty')
async def dota(ctx, ilos):
    red = []
    dupa = ""
    post = open('conf/dota.txt', 'r')
    cip = eval(post.read())
    post.close()
    iloss = int(ilos)
    tmp = []
    if iloss < 20:
        for x in range(iloss):
            while True:
                rand = random.randint(0, len(cip) - 1)
                print(rand)
                if rand not in tmp:
                    break
            red.append(cip[rand])
            tmp.append(rand)
        for y in red:
            dupa += y

        await ctx.channel.send(dupa)
    else:
        await ctx.channel.send("kocham remi?")



@bot.command(help='Pokazuje zakazane slowa')
async def listzakaz(ctx):
    t = []
    await asyncio.sleep(2)
    f = open('conf/ban.txt', 'r')
    t = f.read()
    f.close()
    await ctx.channel.send(t)


@bot.command(help='ping')
async def ping(ctx):
    await ctx.channel.send("ping!")


# @bot.command(help='szuka po numerze')
# async def nkod(ctx, arg):
#     debil = nka.nka()
#     x = debil.numer(arg)
#     await ctx.channel.send(x)
#
# @bot.command(help='szuka po nazwie + ilosc stron')
# async def nszukaj(ctx, arg, arg2=1):
#     debil = nka.nka()
#     x, y = debil.szukaj(arg, arg2)
#     await ctx.channel.send(x)
#     for halo in y:
#         await ctx.channel.send(halo)
#
# @bot.command(help='Wyswietla dojin')
# async def npokaz(ctx, arg):
#     debil = nka.nka()
#     x = debil.druk(arg)
#     await ctx.channel.send(x)

@bot.command(help='kaganiec')
@commands.has_role('MODE BANUJ')
async def kaganiec(ctx, arg1, arg2, arg3):
    role = ctx.guild.get_role(679786116110745600)
    print(role)
    user = arg1
    user = user.replace('<', '')
    user = user.replace('>', '')
    user = user.replace('@', '')
    user = user.replace('!', '')
    print(user)
    iuser = int(user)
    print(iuser)
    usert = ctx.guild.get_member(iuser)
    print(usert)
    arg3 = int(arg3)
    kg.zaloz(user, arg2, arg3)
    await usert.add_roles(role)


@bot.command(help='zmienia status bota')
async def status(ctx, arg):
    await bot.change_presence(activity=discord.Game(arg))
    await ctx.channel.send("ok")


@bot.command(help='myslicie ze co?')
async def remi(ctx, arg):
    channel = bot.get_channel(647798243714924569)
    print(bot.get_user(ctx.author.id))
    await channel.send(arg)



@bot.command()
async def temp(ctx):
    cpu = CPUTemperature()
    a = int(cpu.temperature)
    await ctx.channel.send(f'Temperatura cpu wynosi {a} stopni')





@bot.command(help='pokazuje id')
async def id(ctx, arg):
    print(ctx.author.id)

    print(arg)





@bot.command()
@commands.is_owner()
async def shutdown(ctx):
    await ctx.channel.send('Remiliowych snow')
    await ctx.bot.close()
    
@bot.command()
@commands.is_owner()
async def restart(ctx):
    await ctx.channel.send('Papa')
    os.system('/home/pi/bot/restart.sh')
    await ctx.bot.close()

@commands.is_owner()
@bot.command()
async def update(ctx):
    f = open("wersja.txt")
    wer = str(f.read())
    f.close()
    await ctx.channel.send(f'Aktualna wersja to: {wer}, aktualizujemy!')
    os.system('/home/pi/bot/update.sh')


@bot.command()
async def wersja(ctx):
    f = open("wersja.txt")
    wer = str(f.read())
    f.close()
    await ctx.channel.send(f'Aktualna wersja to: {wer}')


@bot.command()
async def sasiedzi(ctx):
    h = open("conf/somsiedzi.txt", 'r')
    stringi = h.read()
    t = stringi.split()
    h.close()
    p = random.randint(0, len(t))
    await ctx.channel.send(t[p])


# @bot.command(help='Ustawia karte ktora bedzie uzywana przy ataku!')
# async def ustaw(ctx, post):
#     id = ctx.author.id
#     us = mod.User(id)
#     a = us.ustaw(post)
#     await ctx.channel.send(a)
#
#
# @bot.command()
# @commands.cooldown(1, 3600, commands.BucketType.user)
# async def atak(ctx, user2):
#     user1 = str(ctx.author.id)
#     user2 = user2.replace('<', '')
#     user2 = user2.replace('>', '')
#     user2 = user2.replace('@', '')
#     user2 = user2.replace('!', '')
#     if user1 != user2:
#         pos1, pos2 = pvp.get(user1, user2)
#         a = pvp.Pvp(user1, user2)
#         test_str = a.atak(pos1, pos2)
#         await ctx.channel.send(test_str)
#     else:
#         await ctx.channel.send('A wiec jestes samomasochista?')
#
#
# @bot.command()
# async def top(ctx, arg):
#     arg = str(arg)
#     if arg == 'kont':
#         lista = mod.topkon()
#         string = f'Lista 10 najlepszych kont:\n'
#         for x in sorted(lista.keys(), reverse=True):
#             uzyt = lista[x]
#             user = bot.get_user(int(uzyt))
#             string = string + f'{user}, poziom: {x}\n'
#         await ctx.channel.send(string)
#     elif arg == 'touhou':
#         test_str = mod.topdziew()
#         res_first, res_second = test_str[:len(test_str) // 2], test_str[len(test_str) // 2:]
#         res_first1, res_first2 = res_first[:len(res_first) // 2], res_first[len(res_first) // 2:]
#         res_second1, res_second2 = res_second[:len(res_second) // 2], res_second[len(res_second) // 2:]
#         await ctx.channel.send(res_first1)
#         await ctx.channel.send(res_first2)
#         await ctx.channel.send(res_second1)
#         await ctx.channel.send(res_second2)
#
# @bot.command(help='dostajesz losowa karte')
# @commands.cooldown(1, 600, commands.BucketType.user)
# async def los(ctx):
#     id = ctx.author.id
#     us = mod.User(id)
#     a, b = us.los()
#     a = a + f'<@{id}>'
#     b = 'obr/' + b + '.png'
#     await ctx.channel.send(a, file=discord.File(b))
#
#
# @bot.command(help="pokazuje liste posiadanych kart")
# async def list(ctx):
#     id = ctx.author.id
#     us = mod.User(id)
#     a = us.read()
#     a = a + f'<@{id}>'
#     await ctx.channel.send(a)
#
#
# @bot.command(help="przywraca ludzi z limbo")
# async def odlimbo(ctx):
#     id = str(ctx.author.id)
#     dir = 'baza/licznik/' + id + '/'
#     shutil.rmtree(dir, ignore_errors=True)
#     await ctx.channel.send('Zresetowano liczniki!')
#
#
# @bot.command(help='Pokazuje informacje o dziewczynce uzycie %info [dziewczynka]')
# async def info(ctx, arg):
#     id = ctx.author.id
#     arg = arg.lower()
#     us = mod.User(id)
#     a, b = us.pok(arg)
#     a = a + f'<@{id}>'
#     b = 'obr/' + b + '.png'
#     await ctx.channel.send(a, file=discord.File(b))


# @bot.command(help="Wysyla dziewczynke na zadanie, uzycie %quest [dziewczynka]")
# @commands.cooldown(1, tajm, commands.BucketType.user)
# async def quest(ctx, arg):
#     id = ctx.author.id
#     arg = arg.lower()
#     us = mod.User(id)
#     q, status, czas, nag = await us.quest(arg)
#     q = q + f'<@{id}>'
#     await ctx.channel.send(q)
#     if status == 'y':
#         def check(m):
#             global lista
#             lista = m.content.split()
#             wiad = lista[0]
#             return wiad == '%wybierz' and m.channel == ctx.channel and m.author.id == ctx.author.id
#
#         msg = await bot.wait_for('message', timeout=12, check=check)
#         x = int(lista[1])
#         x = x - 1
#         await ctx.channel.send(f'Wybrano zadanie! <@{id}>'.format(msg))
#         await us.zacznij(nag[x], czas[x], arg)
#         await ctx.channel.send(f'{arg} Wykonala zadanie! <@{id}>'.format(msg))
#
#
# @bot.command(help="Pokazuje poziom konta")
# async def poziom(ctx, arg):
#     user = arg
#     user = user.replace('<', '')
#     user = user.replace('>', '')
#     user = user.replace('@', '')
#     user = user.replace('!', '')
#     us = mod.User(user)
#     x, nieuzywanazmienna = us.poziom()
#     await ctx.channel.send(x)
#remizetony

@commands.is_owner()
@bot.command()
async def dodajrmc(ctx, ilosc):
    user = str(ctx.author.id)
    us = rb.User(user)
    x = us.dodaj(ilosc)
    await ctx.channel.send(x)


@bot.command()
@commands.cooldown(1, 5000, commands.BucketType.user)
async def remicoin(ctx):
    i = float(abs(round(np.random.normal(10, 50),2)))
    user = str(ctx.author.id)
    us = rb.User(user)
    x = us.dodaj(i)
    await ctx.channel.send(x)

@bot.command()
async def zalozkontowremibank(ctx):
    user = str(ctx.author.id)
    us = rb.User(user)
    x = us.zaloz()
    await ctx.channel.send(x)

@bot.command()
async def stankonta(ctx):
    user = str(ctx.author.id)
    us = rb.User(user)
    x = us.stan()
    await ctx.channel.send(x)

@bot.command()
async def wplac(ctx, user2, ilosc):
    user1 = str(ctx.author.id)
    user2 = user2.replace('<', '')
    user2 = user2.replace('>', '')
    user2 = user2.replace('@', '')
    user2 = user2.replace('!', '')
    if ilosc == 'nan':
        await ctx.channel.send(f'Debl')
    else:
        if user1 != user2:
            us = rb.User(user1)
            x = us.przelew(user2, ilosc)
            await ctx.channel.send(x)
        else:
            await ctx.channel.send('Nie mozesz tego wykonac')


@bot.command(help='pokazuje statyski RMC')
async def stat(ctx):
    x = rb.plot()
    b = 'bank/stat/fumo.png'
    await ctx.channel.send(x, file=discord.File(b))

@commands.is_owner()
@bot.command()
async def gstart(ctx):
    global aukcja
    x, b = aukcja.start()
    await ctx.channel.send(x, file=discord.File(b))

@commands.is_owner()
@bot.command()
async def gend(ctx):
    global aukcja
    x = aukcja.end()
    await ctx.channel.send(x)

@bot.command(help='Podbija aukcje')
async def bid(ctx, p):
    global aukcja
    p = float(p)
    ok = str(ctx.author.id)
    x = aukcja.bid(p, ok)
    await ctx.channel.send(x)


@bot.command(help='pokazuje kto posiadana dana waifu')
async def ktoma(ctx, p):
    global aukcja
    x = aukcja.sprawdz(p)
    await ctx.channel.send(x)

@bot.command(help='Pokazuje aktualny item na aukcji')
async def cojest(ctx):
    global aukcja
    x = aukcja.zwrot()
    await ctx.channel.send(x)

@bot.command(help='pokazuje co sie ma')
async def list(ctx):
    global aukcja
    x = aukcja.lista(ctx.author.id)
    await ctx.channel.send(x)

@bot.command(help='sprzedaj [komu] [co] [ile]')
async def sprzedaj(ctx, user2, wafu, cena):
    user1 = str(ctx.author.id)
    user2 = user2.replace('<', '')
    user2 = user2.replace('>', '')
    user2 = user2.replace('@', '')
    user2 = user2.replace('!', '')
    if cena == 'nan':
        await ctx.channel.send('DEbil')
    else:


        if user1 != user2:
            await ctx.channel.send('Czekam 12 sekund na %tak od kupującego')
            def check(m):
                global lista
                lista = m.content.split()
                wiad = lista[0]
                return wiad == '%tak' and m.channel == ctx.channel and m.author.id == int(user2)

            msg = await bot.wait_for('message', timeout=12, check=check)
            x = gd.sprzedaj(user1, user2, wafu, cena)
            await ctx.channel.send(x)
        else:
            await ctx.channel.send('Nie mozesz tego wykonac')


@bot.command(help='pokazuje zbudowane generatory')
async def ulepszenia(ctx):
    user = str(ctx.author.id)
    x = gd.Faktoro(user)
    s = x.budynki()
    await ctx.channel.send(s)

@bot.command(help='ulepsza o jeden poziom')
async def ulepsz(ctx, b):
    user = str(ctx.author.id)
    x = gd.Faktoro(user)
    s = x.upgrade(b)
    await ctx.channel.send(s)


@bot.command(help='pokazuje cene ulepszenia')
async def koszt(ctx, b):
    user = str(ctx.author.id)
    x = gd.Faktoro(user)
    s = x.scen(b)
    await ctx.channel.send(s)

@commands.is_owner()
@bot.command()
async def dchd(ctx):
    x = gd.update()
    await ctx.channel.send(x)
@bot.command()
async def dochod(ctx):
    x = gd.spraw(str(ctx.author.id))
    await ctx.channel.send(x)

bot.run(token)
