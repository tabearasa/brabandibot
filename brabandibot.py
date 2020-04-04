import telegram.ext
from telegram.ext import Updater, JobQueue, Job, CallbackContext
from telegram.ext import CommandHandler
import logging
from jokes import joke, tronalddump
from muellcalendar import muellrequest, istodaymuell
import datetime
from datetime import datetime, timedelta, time
from pprint import pprint

#Bot Setup
updater = Updater(token='1093447063:AAEAyXrmud6nG7ahRh3FSZg2D-JCOng_OmM', use_context=True)
dispatcher = updater.dispatcher
muell_que = updater.job_queue
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)



#Send Message
def joke_bot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=joke())

muell = muellrequest()
def muell_bot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=istodaymuell(muell))

def tronalddump_bot(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=tronalddump())


#Command Handler
muell_handler = CommandHandler('muell', muell_bot)
dispatcher.add_handler(muell_handler)

joke_handler = CommandHandler('joke', joke_bot)
dispatcher.add_handler(joke_handler)

tronalddump_handler = CommandHandler('tronalddump', tronalddump_bot)
dispatcher.add_handler(tronalddump_handler)

#Automated Notification Muell
def callback_muell(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='508098654', text='Ihr müsst morgen den gelben Sack rausbringen!')

today_date = datetime.now().date()
today_time = datetime.now()
message = time(hour= 8, minute= 0)
tomorrow = today_date + timedelta(days=1)
muellcal = muellrequest()
muelltime_call=[]

for date in muellcal:
    muelltime_call.append(datetime.combine(date=date - timedelta(days=1), time=message))
else:
    None

muell_que_list = []

for datetime in muelltime_call:
    if datetime > today_time:
        muell_que_list.append(muell_que.run_once(callback=callback_muell, when=datetime))
    else:
        None

print(muellcal)
print(muelltime_call)
print(muell_que_list)

updater.start_polling()