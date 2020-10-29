#!/usr/bin/env python3
import datetime
from datetime import datetime, timedelta, time

import telegram.ext
from telegram import User
from telegram.ext import Updater, JobQueue, Job, CallbackContext, CommandHandler
import logging

from jokes import joke, tronalddump
from muellcalendar import muellrequest, istodaymuell
#from putzplan import putzplan


#Bot Setup
updater = Updater(token='', use_context=True)
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


#Putzplan
def show_putzplan(update, context):
    context.bot.send_message(update.message.chat_id, str(update.message.from_user.first_name)) 

#Command Handler
muell_handler = CommandHandler('muell', muell_bot)
dispatcher.add_handler(muell_handler)

joke_handler = CommandHandler('joke', joke_bot)
dispatcher.add_handler(joke_handler)

tronalddump_handler = CommandHandler('tronalddump', tronalddump_bot)
dispatcher.add_handler(tronalddump_handler)

show_putzplan_handler = CommandHandler('putzplan', show_putzplan)
dispatcher.add_handler(show_putzplan_handler)

#Automated Notification Muell
def callback_muell(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='479197721', text='Ihr müsst morgen den gelben Sack rausbringen!')

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

#Rasenpoints
def rasenpunkte(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="")

updater.start_polling()
