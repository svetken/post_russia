from telegram.ext import Updater, CommandHandler, MessageHandler, filters
from redis import StrictRedis
r = StrictRedis()

# 48826383

def start(bot, update):
	print("Вызван /start")
	bot.sendMessage(update.message.chat_id, text="Welcome to the friendliest service ever - Post of Russia!")

def add(bot, update):
    pochta_add = update.message.text
    pochta_add = pochta_add.split()
    pochta_add = pochta_add[1]
    
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    user_code = r.get(chat_id)
    if user_code is None:
        get_pochta = r.set(chat_id, str(pochta_add))
    else:
        user_code = user_code.decode('utf-8').split(',')
        if pochta_add in user_code:
            bot.sendMessage(update.message.chat_id, text='Вообще-то его мы уже добавили =РРР')
            return
        user_code.append(pochta_add)
        user_code = ','.join(user_code)
        set_pochta = r.set(chat_id, user_code)

def get(bot, update):
	tracking_number = update.message.text.split(" ")[1]
	user_data = r.get('chat_id:'+ str(update.message.chat_id))
	if user_data is None:
		bot.sendMessage(update.message.chat_id, text='nicho net')
		return

	list_of_user_codes = user_code.decode('utf-8').split(',')  # [23, 77, 59]
	bot.sendMessage(update.message.chat_id, text=list_of_user_codes[int(tracking_number) - 1])


def run_bot():
	updater = Updater("302077885:AAEEA-WmwC-2aMfl2ozxr6rsN0lRKnOkiUw")

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("add", add))
	dp.add_handler(CommandHandler("get", get))

	updater.start_polling()
	updater.idle()



if __name__ == "__main__":
	run_bot()