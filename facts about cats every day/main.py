import os
import telebot
from telebot import types
import requests
import schedule
from threading import Thread
from time import sleep
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

bool1 = False

#start
#_____________________________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=["start"], content_types=["text"])
def start(message):
    bot.send_message(message.chat.id, "This is a bot that will send various facts about cats every day")
    with open("ids.txt", "a") as file:
        with open("ids.txt", "r") as file1:
            check = file1.read().splitlines()
            if str(message.chat.id) not in check:
                file.write(f'{message.chat.id}\n')
#____________________________________________________________________________________________________________________________________________________________________
#help
#_____________________________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=["help"], content_types=["text"])
def help(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    fact = types.KeyboardButton("/fact")
    markup.add(fact)
    bot.send_message(message.chat.id, "/fact - random fact obout cats", reply_markup=markup)
#_____________________________________________________________________________________________________________________________________________________________________

#fact
#_____________________________________________________________________________________________________________________________________________________________________
@bot.message_handler(commands=["fact"], content_types=["text"])
def fact(message):
    try:
        bot.send_message(message.chat.id, requests.get("https://catfact.ninja/fact").json()["fact"])
    except:
        bot.send_message(message.chat.id, "something went wrong")
#_____________________________________________________________________________________________________________________________________________________________________

#send fact
#_____________________________________________________________________________________________________________________________________________________________________
def send_fact():
    index_to_send = 0
    with open("ids.txt", "r") as file:
        idlist = file.read().splitlines()
    for index_to_send in range(len(idlist)):
        try:
            bot.send_message(int(idlist[index_to_send]), requests.get("https://catfact.ninja/fact").json()["fact"])
            print("sended")
            index_to_send += 1
        except telebot.apihelper.ApiTelegramException:
            if 0 <= index_to_send < len(idlist):
                del idlist[index_to_send]
                print("deleted")

            with open("ids.txt", "w") as file:
                for el in idlist:
                    file.writelines(f'{el}\n')
            index_to_send +=1 


def schedule_checker():
    while True:
        schedule.run_pending()
        sleep(1)    
#_____________________________________________________________________________________________________________________________________________________________________

if __name__ == "__main__":
    #schedule.every(1).hours.do(send_fact)
    schedule.every().day.at("11:00").do(send_fact)
    #schedule.every(2).minutes.do(send_fact)
    Thread(target=schedule_checker).start() 
    bot.polling(none_stop=True)
