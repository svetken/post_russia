from telegram.ext import Updater, CommandHandler, MessageHandler, filters
import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)
from suds.client import Client


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


def check(bot, update):
    print('Юзер отправляет запрос в Почту России. Боже, сохрани его!')
    bot.sendMessage(update.message.chat_id, text="ну попробуй это прочитать!)))")
    user_barcode = update.message.text.split(" ")[1]
    print(user_barcode)
    url = 'https://tracking.russianpost.ru/rtm34?wsdl'
    client = Client(url, retxml=True, headers={'Content-Type': 'application/soap+xml; charset=utf-8'}, location='https://tracking.russianpost.ru/rtm34/Service.svc')
    barcode = user_barcode
    print(barcode)
    my_login = 'PkFVrNfQbrLZSv'
    my_password = 'RxAkvP1AKeGH'
    print(my_password)
    message = \
"""<?xml version="1.0" encoding="UTF-8"?>
                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:oper="http://russianpost.org/operationhistory" xmlns:data="http://russianpost.org/operationhistory/data" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
   <soap:Header/>
   <soap:Body>
      <oper:getOperationHistory>
         <!--Optional:-->
         <data:OperationHistoryRequest>
            <data:Barcode>""" + barcode+ """</data:Barcode>
            <data:MessageType>0</data:MessageType>
            <!--Optional:-->
            <data:Language>RUS</data:Language>
         </data:OperationHistoryRequest>
         <!--Optional:-->
         <data:AuthorizationHeader soapenv:mustUnderstand="?">
            <data:login>"""+ my_login +"""</data:login>
            <data:password>""" + my_password + """</data:password>
         </data:AuthorizationHeader>
      </oper:getOperationHistory>
   </soap:Body>
</soap:Envelope>"""
    result = client.service.getOperationHistory(__inject={'msg':message})
    result = result.decode('utf-8')
    print(result)
    sFile = open ("otv.txt",'w')
    sFile.write(str(result))
    sFile.close()
    bot.sendMessage(update.message.chat_id, text=result)
    #except Exception as e:
    #   print(e)


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
    print(update.message.text)
    tracking_number = update.message.text.split(" ")[1]
    print(tracking_number)
    user_data = r.get('chat_id:'+ str(update.message.chat_id))
    print(user_data)
    if user_data is None:
        bot.sendMessage(update.message.chat_id, text='nicho net')
        return
    list_of_user_codes = user_data.decode('utf-8').split(',')
    print(list_of_user_codes)
    bot.sendMessage(update.message.chat_id, text=list_of_user_codes[int(tracking_number) - 1])


def run_bot():
    updater = Updater("302077885:AAEEA-WmwC-2aMfl2ozxr6rsN0lRKnOkiUw")

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("add", add))
    dp.add_handler(CommandHandler("get", get))
    dp.add_handler(CommandHandler("info", info))
    dp.add_handler(CommandHandler("check", check))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    run_bot()
