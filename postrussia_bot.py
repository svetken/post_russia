from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

def start(bot, update):
	print("Вызван /start")
	bot.sendMessage(update.message.chat_id, text="Welcome to the friendliest service ever - Post of Russia!")

def add(bot, update):
    print('Добавление почтового отправления')
    pochta_add = update.message.text
    pochta_add = pochta_add.split()
    pochta_add = pochta_add[1]
    print(pochta_add)
    
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    #user_data = r.set(str(chat_id), str(pochta_add))
    print(chat_id)
    user_code = r.get(chat_id)
    print(user_code)
    if user_code is None:
        get_pochta = r.set(chat_id, str(pochta_add))
        print(get_pochta)
    else:
        user_code = user_code.decode('utf-8').split(',')
        if pochta_add in user_code:
            bot.sendMessage(update.message.chat_id, text='Вообще-то его мы уже добавили =РРР')
            return
        user_code.append(pochta_add)
        user_code = ','.join(list(set(user_code)))
        set_pochta = r.set(chat_id, user_code)
        print(set_pochta)
    bot.sendMessage(update.message.chat_id, text='Всё добавили, теперь будем следить')


def run_bot():
	updater = Updater("302077885:AAEEA-WmwC-2aMfl2ozxr6rsN0lRKnOkiUw")

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("add", add))

	updater.start_polling()
	updater.idle()



if __name__ == "__main__":
	run_bot()