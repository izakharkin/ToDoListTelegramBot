from telegram.ext import MessageHandler, Filters
from telegram.ext import CommandHandler
from telegram.ext import Updater

import random
import datetime
import time
import logging
import peewee

updater = Updater(token='345673297:AAEkO7V3iWAGUUiGLHJHtx3_EOARHCQRpc0')
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger()

HELP_INFO = 'Hello! I am the ToDoList Bot.\n' \
            'I can help you to organize your events, ' \
            'keep track of your deadlines ' \
            'and even tell the joke ;)' \
            'Use this commands:\n' \
            '/help - list all available commands\n' \
            '/add <name> <date> <time> - add new event or deadline, where:\n' \
            '<name> - some name for your event or deadline,\n' \
            '<date> - date in format dd.mm.yyyy or dd/mm/yyyy\n' \
            '<time> - [optional, if date is present] time in format hh:mm\n' \
            '/remove <event_id> - remove event or deadline (to see the ID`s of events type /show)\n' \
            '/show - show all your events and deadlines (with its ID`s)\n' \
            '/joke - you can try to ask me for a joke, heh :)'

XKCD_MAX_COMICS_NUMBER = 1833


class DBMS:
    ID = 0

    def __init__(self):
        self.db = {}

    class Entry:
        def __init__(self, list_of_fields):
            self.name = list_of_fields[0]
            self.date = list_of_fields[1]
            self.time = list_of_fields[2]

        def __str__(self):
            return ' '.join([self.name, self.date, self.time])

    def insert(self, chat_id, name, date, time):
        event_id = self.ID
        self.ID += 1
        self.db[chat_id][event_id] = self.Entry([name, date, time])

    def remove(self, chat_id, event_id):
        removed_value = self.db.pop((chat_id, event_id))  # can be used
        self.ID -= 1

    def get_all_todos(self, chat_id):
        events = [entry for entry in self.db[chat_id]]
        return '\n'.join(events)


dbms = DBMS()


# COMMANDS

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text="I'm a TODOList Bot, please talk to me!")
    logger.log(msg='session started: time={} chat_id={}'.format(time.clock(), update.message.chat_id))


def echo(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=update.message.text)


def help(bot, update):
    help_text = HELP_INFO
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=help_text)
    logger.log(msg='')


class TooMuchDateArgumentsException(Exception):
    def __init__(self):
        super.__init__()


class TooMuchTimeArgumentsException(Exception):
    def __init__(self):
        super.__init__()


class DateType:
    def __init__(self, date_string):
        # can be handled by a fabric method,
        # but here I`ll just do it "in-place"
        now = datetime.datetime.now()
        day = now.day
        month = now.month
        year = now.year

        tokens = date_string.split('.\/')

        if (len(tokens) > 3):
            raise TooMuchDateArgumentsException()

        if (len(tokens) >= 1):
            day = tokens[0]
            if (len(tokens) >= 2):
                month = tokens[1]
                if (len(tokens) == 3):
                    year = tokens[2]
        try:
            datetime._check_date_fields(year, month, day)
        except Exception:
            print('Wrong day, month or year. TODO is not added :(')

        self.day = day
        self.month = month
        self.year = year

    def __str__(self):
        return '.'.join([self.day, self.month, self.year])


class TimeType():
    def __init__(self, time_string):
        hour = 0
        minute = 0

        tokens = time_string.split(':')

        if (len(tokens) > 2):
            raise TooMuchTimeArgumentsException()

        if (len(tokens) >= 1):
            hour = tokens[0]
            if (len(tokens) == 2):
                minute = tokens[1]

        # check correctness of time

        self.hour = hour
        self.minute = minute


class TooFewParseArgumentsException(Exception):
    def __init__(self):
        super.__init__()


class WrondIdException(Exception):
    def __init__(self):
        super.__init__()


class Parser:
    @staticmethod
    def parse_event(self, event_string):
        tokens = event_string.split(' ')

        if (len(tokens) < 2):
            raise TooFewParseArgumentsException()

        name = ' '.join(tokens[:-2])
        date = DateType(tokens[-2])
        time = TimeType(tokens[-1])

        return name, date, time

    @staticmethod
    def parse_id(self, event_id):
        tokens = int(event_id)
        return tokens[0]


def add_event(chat_id, event_string):
    name, date, time = Parser.parse_event(event_string)
    dbms.insert(chat_id, name, date, time)


def add(bot, update):
    add_event(update.message.chat_id, update.message.text)
    success_text = 'New TODO successfully added'
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=success_text)
    logger.log(msg='chat_id={} time={} operation=add - successfully added'.format(update.message.chat_id, time.clock()))


def remove_event(chat_id, todo_id):
    event_id = Parser.parse_id(todo_id)
    dbms.remove(chat_id, event_id)


def remove(bot, update):
    remove_event(update.message.chat_id, update.message.text)
    success_text = 'TODO successfully removed'
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=success_text)
    logger.log(
        msg='chat_id={} time={} operation=remove - successfully removed'.format(update.message.chat_id, time.clock()))


def show(bot, update):
    print('All your TODO`s:\n')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=dbms.get_all_todos(update.message.chat_id))
    logger.log(
        msg='chat_id={} time={} operation=show - successfully shown'.format(update.message.chat_id, time.clock()))


def generate_joke_from_xkcd():
    return 'https://xkcd.com/{}/'.format(random.randint(XKCD_MAX_COMICS_NUMBER))


def joke(bot, update):
    jokes = []
    jokes.append(generate_joke_from_xkcd)
    jokes.append('So.. Joke, yeah.. A-ha.. Sorry, but I don`t have a joke for now :(')
    bot.sendMessage(chat_id=update.message.chat_id,
                    text=jokes[random.randint(len(jokes))])
    logger.log(
        msg='chat_id={} time={} operation=joke - successfully joked'.format(update.message.chat_id, time.clock()))


# TODO: learn how to handle timer process (how to show messages in time)
# TODO: send messages about deadlines befor 5, 3, 1 days and before 12 hours, 6 hours, 3 hours, 1 hour, 30 minutes..
# TODO: ..according to the 'importance level'

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)

help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)

add_handler = CommandHandler('add', add)
dispatcher.add_handler(add_handler)

remove_handler = CommandHandler('remove', remove)
dispatcher.add_handler(remove_handler)

show_handler = CommandHandler('show', show)
dispatcher.add_handler(show_handler)

joke_handler = CommandHandler('joke', joke)
dispatcher.add_handler(joke_handler)

updater.start_polling()
