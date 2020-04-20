#!/usr/bin/env python3
import datetime
from datetime import datetime, timedelta, time

import telegram.ext
from telegram import User, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, JobQueue, Job, CallbackContext, CommandHandler, CallbackQueryHandler
import logging

from jokes import joke, tronalddump
from muellcalendar import muellrequest, istodaymuell
#from putzplan import putzplan


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
def callback_muell(update, context: telegram.ext.CallbackContext):
    keyboard = [InlineKeyboardButton("Erledigt", callback_data='1')]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Morgen wird der gelbe Sack abgeholt! Ihr müsst den gelben Sack heute oder morgen früh rausstellen.', reply_markup=reply_markup)

    #context.bot.send_message(chat_id='508098654', text='Ihr müsst morgen den gelben Sack rausbringen!')

def button(update, context):
    query = update.callback_query

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    username = query.from_user.username
    message = username + " hat ihn schon rausgestellt."

    query.edit_message_text(text="Morgen wird der gelbe Sack abgeholt!" + message)


#Callback Query Handler (inline buttons)
updater.dispatcher.add_handler(CallbackQueryHandler(button))

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

""" #Automated Notification Rasen
def callback_rasen(context: telegram.ext.CallbackContext):
    context.bot.send_message(chat_id='508098654', text='Wer gießt morgen den Rasen? Nicht vergessen: 1x morgens und 1x abends')

rasen_message_time = time(hour=18, minute=00)
rasen_dates =[today_date + timedelta(days=x) for x in range(14)]
rasen_que_list = []

for date in rasen_dates:
        rasen_que_list.append(rasen_que.run_once(callback=callback_rasen, when= datetime.combine(date=date, time=rasen_message_time) - timedelta(hours=2) )) #2 Stunden abziehen wegen UTC
 """
#Rasenpoints
def rasenpunkte(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="")


updater.start_polling()
