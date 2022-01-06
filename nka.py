import NHentai as nhentai
class nka:
    def __init__(self):
        self.n = nhentai.nhentai.NHentai()

    def numer(self, kod):
        a = self.n.get_doujin(kod)
        tagi = f'Tagi:'
        for x in a.tags:
            tagi += f' {x},'

        char = f'Postacie:'
        for x in a.characters:
            char += f' {x},'

        img = []
        for x in a.images:
            img.append(x)


        stren = f'Wyniki dla {kod}\n {a.title}\n {tagi}\n {char}\n Strony: {a.total_pages}\n Link: https://nhentai.net/g/{kod} \n {img[0]} '

        return stren

    def druk(self, kod):
        a = self.n.get_doujin(kod)
        img = f''
        for x in a.images:
            img += f'{x}\n'
        return img



    def szukaj(self, quer, stron=1):
        a = self.n.search(query=quer, page=stron)
        stren = f'Strona {stron} z {a.total_pages} dla {quer}, {a.total_results} wyników:\n'

        tab=[]
        for x in a.doujins:
            tmp = f''
            tmp += f'{x.id} - {x.title} {x.url}\n'
            tmp += f'\n {x.cover}\n'
            tab.append(tmp)
        return stren, tab



if __name__ == "__main__":
    a = nka()
    print(a.numer("358243"))
    print(a.druk('358243'))
    print(a.szukaj("flandre", '2'))