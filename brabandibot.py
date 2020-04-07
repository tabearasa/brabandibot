import logging
import datetime
from datetime import datetime, timedelta, time
from uuid import uuid4

import telegram.ext
from telegram import User,Updater, JobQueue, Job, CallbackContext, CommandHandler

from jokes import joke, tronalddump
from muellcalendar import muellrequest, istodaymuell

#Bot Setup
updater = Updater(token='1093447063:AAEAyXrmud6nG7ahRh3FSZg2D-JCOng_OmM', use_context=True)
dispatcher = updater.dispatcher
muell_que = updater.job_queue
rasen_que = updater.job_queue
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

#Error Handler
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

dispatcher.add_error_handler(error)

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

#Automated Notification Rasen
def callback_rasen(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='508098654', text='Wer gießt morgen den Rasen? Nicht vergessen: 1x morgens und 1x abends')

rasen_message_time = time(hour=18, minute=00)
rasen_dates =[today_date + timedelta(days=x) for x in range(14)]
rasen_que_list = []

for date in rasen_dates:
        rasen_que_list.append(rasen_que.run_once(callback=callback_rasen, when= datetime.combine(date=date, time=rasen_message_time) - timedelta(hours=2) )) #2 Stunden abziehen wegen UTC


updater.start_polling()