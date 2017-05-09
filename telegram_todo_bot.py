import collections
from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import Updater

import logging, logging.config
import random
# import peewee

import billing
from utils.parser import Parser

# ================ GETTING UPDATER AND DISPATCHER =============

updater = Updater(token='345673297:AAEkO7V3iWAGUUiGLHJHtx3_EOARHCQRpc0')
dispatcher = updater.dispatcher

# ================ LOGGER CONFIGURATION =================

logging.config.fileConfig(fname='log.conf')

# [handler_handler3]
# class=handlers.SMTPHandler
# level=CRITICAL
# formatter=formatter1
# args=('ilyazaharkin@yandex.ru','Critical error found')

log = logging.getLogger('main')

# =============== CONSTANTS ====================

HELP_INFO = 'Hello! I am the TODO List Bot.\n' \
            'I can help you to organize your events, ' \
            'keep track of your deadlines ' \
            'and even tell the joke ;)\n' \
            'Use this commands:\n' \
            '/help - list all available commands\n' \
            '/add <name> <date> <time> - add new event or deadline, where:\n' \
            '<name> - some name for your event or deadline,\n' \
            '<date> - date in format dd.mm.yyyy or dd/mm/yyyy\n' \
            '<time> - [optional if date is present] time in format hh:mm\n' \
            '/remove <event_id> - remove event or deadline (to see the ID`s of events type /show)\n' \
            '/show - show all your events and deadlines (with its ID`s)\n' \
            '/joke - you can try to ask me for a joke, heh :)'

XKCD_MAX_COMICS_NUMBER = 1833

# ================ DATA STORAGE CONFIGURATION =============

dbms = billing.DBMS()


# ================== COMMANDS ==================

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="I'm a TODOList Bot, please talk to me!")
    log.info('bot started in chat_id={}'.format(update.message.chat_id))


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=update.message.text)
    log.debug('/echo in chat_id={}'.format(update.message.chat_id))


def help(bot, update):
    help_text = HELP_INFO
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=help_text)
    log.debug('/help called in chat_id={}'.format(update.message.chat_id))


def add_event(chat_id, event_string):
    try:
        name, date, time_ = Parser.parse_event(event_string)
        event_id = dbms.insert(chat_id, name, date, time_)
    except Exception:
        return 'Wrong /add arguments! Type /help for format information'
    return 'Your TODO is added with ID={}'.format(event_id)


def add(bot, update):
    msg_text = add_event(update.message.chat_id, update.message.text)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=msg_text)
    log.info('/add called in chat_id={}, message: {}'.format(update.message.chat_id, msg_text))


def remove_event(chat_id, event_id):
    parsed_event_id = Parser.parse_id(event_id)
    return dbms.remove(chat_id, parsed_event_id)


def remove(bot, update):
    removed_id = remove_event(update.message.chat_id, update.message.text)
    success_text = 'TODO with ID={} successfully removed'.format(removed_id)
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=success_text)
    log.info('TODO with ID={} removed in chat_id={}'.format(removed_id, update.message.chat_id))


def show(bot, update):
    pretext = 'You have no TODO`s yet. Lucky one!'
    events_text = dbms.get_all_events(update.message.chat_id)
    if events_text != '':
        pretext = 'All your TODO`s:\n'
    msg_text = pretext + events_text
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=msg_text)
    log.debug('/show called in chat_id={}'.format(update.message.chat_id))


def generate_joke_from_xkcd():
    return 'https://xkcd.com/{}/'.format(random.randint(1, XKCD_MAX_COMICS_NUMBER))


def joke(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=generate_joke_from_xkcd())
    log.debug('/joke called in chat_id={}'.format(update.message.chat_id))


# ==================== REMINDER SECTION ===================

# это должен делать отдельный поток
#
# class Reminder: # Singleton
#     def __init__(self, events_dict=collections.OrderedDict()):
#         self.events_queue = events_dict # ordered by ((1)date, (2)time)
#
#     def insert_event(self, event_date, event_time, event_chat_id, event_id):
#         self.events_queue[(event_date, event_time)] = (event_chat_id, event_id)
#
#     def start_tracking(self):
#         while True:
#             current = self.events_queue.front()
#             current_date = datetime.GET_DATE
#             current_time = time.GET_TIME
#


# ==================== ADDING HANDLERS ==============

# TODO: send messages about deadlines befor 5, 3, 1 days and before 12 hours, 6 hours, 3 hours, 1 hour, 30 minutes..
# TODO: ..according to the 'importance level'
# TODO: make buttons when add, remove; help button
# TODO: make scrollable list of events when /show
# TODO: Do I need a MySQL DB?
# TODO: deploy on Heroku (when all is ready)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

add_handler_ = CommandHandler('add', add)
dispatcher.add_handler(add_handler_)

remove_handler = CommandHandler('remove', remove)
dispatcher.add_handler(remove_handler)

show_handler = CommandHandler('show', show)
dispatcher.add_handler(show_handler)

joke_handler = CommandHandler('joke', joke)
dispatcher.add_handler(joke_handler)

# =================== START THE SCRIPT ==============

updater.start_polling()
