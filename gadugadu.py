from chatterbot import ChatBot


bot = ChatBot('Remilia', database_uri='sqlite:///database.sqlite3')

def wiad(msg):
    try:
        odp = bot.get_response(msg)
        return odp
    except: return  f'Jaki blad czy cos sry'