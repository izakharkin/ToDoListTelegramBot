import logging, logging.config
import random

from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import Updater

from billing import DBMS
from tracker import Tracker
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

dbms = DBMS()

# ==================== NOTIFICATION SYSTEM ===================

# это должен делать отдельный поток

notifier = Tracker()


# ================== COMMANDS ==================

def start(bot, update):
    start_text = HELP_INFO
    bot.sendMessage(chat_id=update.message.chat_id, text=start_text)
    log.info('bot started in chat_id={}'.format(update.message.chat_id))


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=update.message.text)
    log.debug('/echo in chat_id={}'.format(update.message.chat_id))


def help(bot, update):
    help_text = HELP_INFO
    bot.sendMessage(chat_id=update.message.chat_id, text=help_text)
    log.debug('/help called in chat_id={}'.format(update.message.chat_id))


def add_event(chat_id, event_string):
    name, date, time_ = Parser.parse_event(event_string)
    event_id = dbms.insert(chat_id, name, date, time_)
    # notifier.insert_event(date, time_, chat_id, event_id)
    return event_id


def add(bot, update):
    try:
        event_id = add_event(update.message.chat_id, update.message.text)
        msg_text = 'Your TODO is added with ID={}'.format(event_id)
    except Exception:
        msg_text = 'Wrong event parameters. Type /help for format information.'
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_text)
    log.info('/add called in chat_id={}, message: {}'.format(update.message.chat_id, msg_text))


def remove_event(chat_id, event_id):
    parsed_event_id = Parser.parse_id(event_id)
    removed_id = dbms.remove(chat_id, parsed_event_id)
    return removed_id


def remove(bot, update):
    try:
        removed_id = remove_event(update.message.chat_id, update.message.text)
        msg_text = 'TODO with ID={} succssfully removed'.format(removed_id)
    except Exception:
        msg_text = 'Wrong ID or event with this ID doesn`t exist. Type /show for events list.'
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_text)
    log.info('/remove called in chat_id={}, message: {}'.format(update.message.chat_id, msg_text))


def show(bot, update):
    pretext = 'You have no TODO`s yet. Lucky one!'
    events_text = dbms.get_all_events(update.message.chat_id)
    if events_text != '':
        pretext = 'All your TODO`s:\n'
    msg_text = pretext + events_text
    bot.sendMessage(chat_id=update.message.chat_id, text=msg_text)
    log.debug('/show called in chat_id={}'.format(update.message.chat_id))


def generate_joke_from_xkcd():
    return 'https://xkcd.com/{}/'.format(random.randint(1, XKCD_MAX_COMICS_NUMBER))


def joke(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=generate_joke_from_xkcd())
    log.debug('/joke called in chat_id={}'.format(update.message.chat_id))


# ==================== ADDING HANDLERS =================

# TODO: /clear - delete old TODO's
# TODO: make buttons when add, remove; help button
# TODO: make scrollable list of events when /show
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
