from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext, Filters

from key import TOKEN

import requests
import logging

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s: %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def main():
    updater = Updater(token=TOKEN)
    dp: Dispatcher = updater.dispatcher

    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', get_help))
    dp.add_handler(CommandHandler('cat', get_cat))
    dp.add_handler(CommandHandler('dog', get_dog))
    dp.add_handler(CommandHandler('menu', menu))
    dp.add_handler(CommandHandler('timetable', timetable))
    dp.add_handler(CallbackQueryHandler(table_react))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


def start(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} вызвал функцию start')

    text = [
        f'Добрый день/вечер/утро, <code>{update.effective_user.username}</code>!',
        f'',
        f'Приветствую <b>Вас</b> в моем боте <b>kgpebbot</b>!',
        f'Что он умеет, <i>вы можете узнать</i>, написав команду /help',
        f'',
        f'<b>Приятного времени провождения :)</b>'
    ]
    text = '\n'.join(text)

    update.message.reply_text(text, parse_mode=ParseMode.HTML)


def get_help(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} вызвал команду do_help')

    text = [
        f'Раздел <b>H E L P</b>',
        f'',
        f'Этот <b>бот</b> сделан пользователем (weldoy)',
        f'Если кому-то интересно, вот мой <a href="github.com/weldoy">GitHub</a> :3',
        f'Предназначен для развлечений :)',
        f'',
        f'Чтобы узнать <b>полный функционал</b>, напишите /menu'
    ]
    text = '\n'.join(text)

    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


def unknown(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} ввел неправильную команду')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Извините, я не знаю, что это :/")


def menu(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    logger.info(f'{user_id=} вызвал меню')
    buttons = [
        ['/cat', '/dog'],
        ['/timetable'],
    ]
    text = 'Выберайте то, что вам нужно :)'
    keyboard = ReplyKeyboardMarkup(buttons)
    update.message.reply_text(text, reply_markup=keyboard)


def timetable(update: Update, context: CallbackContext):
    logger.info(f"{update.effective_user.username} Bызвaл функцию do_inline_keyboard")
    buttons = [
        ['monday', 'tuesday'],
        ['wednesday', 'thursday'],
        ['friday']
    ]
    keyboard_button = [[InlineKeyboardButton(text=text, callback_data=text) for text in row] for row in buttons]
    keyboard = InlineKeyboardMarkup(keyboard_button)
    text = f'Выберите <b>день</b>, для которого Вам нужно <b>расписание</b> :)'
    update.message.reply_text(text, reply_markup=keyboard, parse_mode=ParseMode.HTML)


def table_react(update: Update, context: CallbackContext):
    query = update.callback_query
    logger.info(f'{update.effective_user.username} вызвал функцию keyboard_react')
    if query.data == 'monday':
        logger.info(f'{update.effective_user.username} вызвал функцию monday')
        img1 = 'https://imgur.com/mQ2ICKI'
        context.bot.send_message(update.effective_chat.id, 'Ваше расписание!',
                                 reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(update.effective_chat.id, img1)

    if query.data == 'tuesday':
        logger.info(f'{update.effective_user.username} вызвал функцию tuesday')
        img2 = 'https://imgur.com/UnzRRGX'
        context.bot.send_message(update.effective_chat.id, 'Ваше расписание!',
                                 reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(update.effective_chat.id, img2)

    if query.data == 'wednesday':
        logger.info(f'{update.effective_user.username} вызвал функцию wednesday')
        img3 = 'https://imgur.com/WHtzRFu'
        context.bot.send_message(update.effective_chat.id, 'Ваше расписание!',
                                 reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(update.effective_chat.id, img3)

    if query.data == 'thursday':
        logger.info(f'{update.effective_user.username} вызвал функцию thursday')
        img4 = 'https://imgur.com/ZvMeJUd'
        context.bot.send_message(update.effective_chat.id, 'Ваше расписание!',
                                 reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(update.effective_chat.id, img4)

    if query.data == 'friday':
        logger.info(f'{update.effective_user.username} вызвал функцию friday')
        img5 = 'https://imgur.com/OWXN3fH'
        context.bot.send_message(update.effective_chat.id, 'Ваше расписание!',
                                 reply_markup=ReplyKeyboardRemove())
        context.bot.send_photo(update.effective_chat.id, img5)


ERROR_MESSAGE = 'Ошибка при запросе к основному API: {error}'
URL = 'https://api.thecatapi.com/v1/images/search'
DOGS_URL = 'https://api.thedogapi.com/v1/images/search'
RESPONSE_USERNAME = 'Картинку {image_name} запросил: {username}, {name}'


def get_new_image():
    try:
        response = requests.get(URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = DOGS_URL
        response = requests.get(new_url)

    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_cat(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='котека',
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image(),
                           reply_markup=ReplyKeyboardRemove())


def get_new_image2():
    try:
        response = requests.get(DOGS_URL)
    except Exception as error:
        logging.error(ERROR_MESSAGE.format(error=error))
        new_url = URL
        response = requests.get(new_url)

    response = response.json()
    random_dog = response[0].get('url')
    return random_dog


def get_dog(update, context):
    chat = update.effective_chat
    logging.info(RESPONSE_USERNAME.format(
        image_name='пес',
        username=chat.username,
        name=chat.first_name
    ))
    context.bot.send_photo(chat.id, get_new_image2(),
                           reply_markup=ReplyKeyboardRemove())


if __name__ == '__main__':
    main()
