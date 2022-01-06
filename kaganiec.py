import datetime

def zaloz(user, typ, czas):
    tab = []
    now = datetime.datetime.now()
    if typ == 'd':
        dni = czas
        w = now + datetime.timedelta(days=dni)
        koniec = w.strftime("%Y-%m-%d:%H:%M")

    elif typ == 'h':
        godz = czas
        w = now + datetime.timedelta(hours=godz)
        koniec = w.strftime("%Y-%m-%d:%H:%M")

    elif typ == 'm':
        min = czas
        w = now + datetime.timedelta(minutes=min)
        koniec = w.strftime("%Y-%m-%d:%H:%M")
    else:
        return
    f = open('kaganiec/list.txt', 'r')
    tab = eval(f.read())
    f.close()
    tab.append(user + '=' + koniec)
    f = open('kaganiec/list.txt', 'w')
    f.write(str(tab))
    f.close()


def zdejmij(user):
    t = []
    a = []
    f = open('kaganiec/list.txt', 'r')
    plik = f.read()
    t = eval(plik)
    for x in t:
        a = x.split('=')
        if a[0] == user:
            t.remove(x)
    f.close()
    f = open('kaganiec/list.txt', 'w')
    f.write(str(t))
    f.close()
