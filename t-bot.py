import telebot
import config
import os
import sqlite3
import pandas
import time

from zipfile import *


bot = telebot.TeleBot(config.TOKEN)
conn = sqlite3.connect('ufiles.db', check_same_thread=False)
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   userid INTEGER,
   fname TEXT);
""")
conn.commit()
cur.execute("""CREATE TABLE IF NOT EXISTS uid(
   userid INTEGER);
""")
conn.commit()
@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    user = message.from_user.username
    cur.execute("select * from uid")
    u = cur.fetchall()
    udb = str(uid)
    print(udb)
    print([uid])
    if udb not in u:
        cur.execute("INSERT INTO uid VALUES(?);", [udb])
        conn.commit()
    print(user," ",uid)
    cur.execute("select * from uid")
    print(cur.fetchall())
    print(message.text)
    dir = os.path.abspath(os.curdir)
    bot.send_message(message.chat.id, "Добро пожаловать, я парсер твоих логов на наличие Discord токенов".format(message.from_user, bot.get_me()),
        parse_mode='html')
    bot.send_message(message.chat.id, "Кодер - @proporcia5")

#@bot.message_handler(content_types=['text'])
#def message(message):
#    uid = message.from_user.id
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        uid = message.from_user.id
        chat_id = message.chat.id
        dir = os.path.abspath(os.curdir)
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file = message.document.file_name
        src = dir + "/files/" + message.document.file_name;
        src = src.replace("\\", "/")
        filesdb = [uid, file]
        print(filesdb,"fdsaf")
        ulist = uid
        if file.endswith(".zip"):
            print("ayam")
            with open(src, 'wb') as new_file:
                new_file.write(downloaded_file)
            cur.execute("INSERT INTO users VALUES(?, ?);", filesdb)
            conn.commit()
            print("db upload")
            bot.reply_to(message, "Успех")
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFlWZi-6eD2Ep-XFvK713oGB19afSXBAAC8AwAAkLRyUgtqT9JY9FGmCkE")
            cur.execute("SELECT * FROM users WHERE userid = ?;", [ulist])
            one_result = cur.fetchone()
            print(one_result)
            archive = dir + '/files/' + one_result[1]
            print(archive)
            import zipfile
            with ZipFile(archive) as myzip:
                for items in myzip.namelist():
                    print(items)
                    f = items.find('Cookies')
                    if f == -1:
                        if items[-4:] =='.txt':
                            print('ok')
                            with zipfile.ZipFile(archive) as thezip:
                                with thezip.open(items ,mode='r') as thefile:
                                    m = thefile.read()
                                    bot.send_message(chat_id, 'Файл с директории '+ items)
                                    if len(m) == 0:
                                        bot.send_message(chat_id, 'Файл пустой')
                                        time.sleep(2)
                                    elif len(m) > 4090:
                                        for x in range(0, len(m), 4090):
                                            bot.send_message(chat_id, text=m[x:x+4090])
                                            time.sleep(2)
                                    else:
                                        bot.send_message(chat_id, text=m)
                                        time.sleep(2)
            cur.execute("SELECT * FROM users")
            print(cur.fetchall())
            print('delete')
            os.remove(archive)
            bot.send_message(chat_id, 'всё логи чекнул')
            cur.execute("DELETE FROM users WHERE fname = ? ;", [file])
            conn.commit()
            cur.execute("SELECT * FROM users")
            print(cur.fetchall())
        #elif file.endswith(".rar"):
        #    print("1ayam")
        #    with open(src, 'wb') as new_file:
        #        new_file.write(downloaded_file)
        #    cur.execute("INSERT INTO users VALUES(?, ?);", filesdb)
        #    conn.commit()
        #    print("db upload")
        #    bot.reply_to(message, "Успех")
        #    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFlWZi-6eD2Ep-XFvK713oGB19afSXBAAC8AwAAkLRyUgtqT9JY9FGmCkE")
        #    cur.execute("SELECT * FROM users WHERE userid = ?;", [ulist])
        #    one_result = cur.fetchone()
        #    print(one_result)
        else:
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFlWRi-6cG2hB7KgnQLrivZGK-VhE7twAC4wkAAt3AKEgBhV6Pkmz_SCkE")
            bot.send_message(chat_id, "Поддержка только .zip архивов, .rar в разработке")
    except Exception as e:
        bot.reply_to(message, e)






bot.polling(none_stop=True)
