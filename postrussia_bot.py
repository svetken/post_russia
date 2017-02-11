from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

# 48826383

def start(bot, update):
    print("Вызван /start")
    bot.sendMessage(update.message.chat_id, text="Welcome to the friendliest service ever - Post of Russia!")

def info(bot, update):
    print('Пользователь интересуется, а что это он там ждет от Почты России')
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    pochta_info = r.get(chat_id)
    pochta_info = pochta_info.decode('utf-8').split(',')
    print(pochta_info)
    pochta_result = ''
    for i, element in enumerate(pochta_info):
        pochta_result += ('{}. {}'.format(i+1, element))
        pochta_result += '\n'
    bot.sendMessage(update.message.chat_id, text=pochta_result)



def add(bot, update):
    print('Добавление почтового отправления')
    pochta_add = update.message.text
    pochta_add = pochta_add.split()
    pochta_add = pochta_add[1]
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    user_code = r.get(chat_id)
    if user_code is None:
        get_pochta = r.set(chat_id, str(pochta_add))
        print(get_pochta)
    else:
        user_code = user_code.decode('utf-8').split(',')
        if pochta_add in user_code:
            bot.sendMessage(update.message.chat_id, text='Вообще-то его мы уже добавили =РРР')
            return
        user_code.append(pochta_add)
        user_code = ','.join(user_code)
        set_pochta = r.set(chat_id, user_code)
    bot.sendMessage(update.message.chat_id, text='Всё добавили, теперь будем следить')

def get(bot, update):
    tracking_number = update.message.text.split(" ")[1]
    user_data = r.get('chat_id:'+ str(update.message.chat_id))
    if user_data is None:
        bot.sendMessage(update.message.chat_id, text='nicho net')
        return

    list_of_user_codes = user_data.decode('utf-8').split(',')  # [23, 77, 59]
    bot.sendMessage(update.message.chat_id, text=list_of_user_codes[int(tracking_number) - 1])

def info(bot, update):
    print('Пользователь интересуется, а что это он там ждет от Почты России')
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    pochta_info = r.get(chat_id)
    pochta_info = pochta_info.decode('utf-8').split(',')
    print(pochta_info)
    pochta_result = ''
    for i, element in enumerate(pochta_info):
        pochta_result += ('{}. {}'.format(i+1, element)) 
        pochta_result += '\n'
    bot.sendMessage(update.message.chat_id, text=pochta_result)

def delete(bot, update):
    chat_id = 'chat_id:'+ str(update.message.chat_id)
    list_of_parcels = r.get(chat_id)
    list_of_parcels.split(' ')
    bot.sendMessage(update.message.chat_id, text='Here is your current list: ' + ', '.join(list_of_parcels))

    what_to_del = input('Which one do you wanna delete? ')
    if int(what_to_del) > len(list_of_parcels):
        bot.sendMessage(update.message.chat_id, text='wtf are you doing?')
    elif int(what_to_del) <= 0:
        bot.sendMessage(update.message.chat_id, text='Nothing to delete')
    else:
        del list_of_parcels[int(what_to_del) - 1]
    
    text = 'Okay. Thats what you have for now: '

    bot.sendMessage(update.message.chat_id, text=text + ', '.join(list_of_parcels))







def run_bot():
	updater = Updater("302077885:AAEEA-WmwC-2aMfl2ozxr6rsN0lRKnOkiUw")

	dp = updater.dispatcher
	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("add", add))
	dp.add_handler(CommandHandler("get", get))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("delete", delete))
    dp.add_handler(CommandHandler("info", add))
>>>>>>> c6d719952abd48900d05d9fd8910cb2872a42029

	updater.start_polling()
	updater.idle()

if __name__ == "__main__":
    run_bot()
