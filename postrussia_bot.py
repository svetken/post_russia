from telegram.ext import Updater, CommandHandler, MessageHandler, filters

def start(bot, update):
	print("Вызван /start")
	bot.sendMessage(update.message.chat_id, text="Welcome to the friendliest service ever - Post of Russia!")

def add(bot, update)
	bot.sendMessage(update.message.chat_id, text="stay tuned")


def run_bot():
	updater = Updater("302077885:AAEEA-WmwC-2aMfl2ozxr6rsN0lRKnOkiUw")

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("add", add))

	updater.start_polling()
	updater.idle()



if __name__ == "__main__":
	run_bot()