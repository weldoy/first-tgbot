from telegram import Update, ParseMode
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Dispatcher, MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import CallbackContext, Filters

from key import TOKEN

import logging
import datetime

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
    dp.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()


def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    username = update.effective_user.username

    logger.info(f'{username} вызвал функцию start')

    text = [
        f'Добрый день/вечер/утро, <code>{username}</code>!',
        f'',
        f'Приветствую <b>Вас</b> в моем боте <b>kgpebbot</b>!',
        f'Что он умеет, <i>вы можете узнать</i> написав команду /help',
        f'',
        f'<b>Приятного времени провождения :)</b>'
    ]
    text = '\n'.join(text)

    update.message.reply_text(text, parse_mode=ParseMode.HTML)


def unknown(update: Update, context: CallbackContext):
    logger.info(f'{update.effective_user.username} ввел неправильную команду')
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Извините, я не знаю, что это :/")


def get_help(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id

    logger.info(f'{user_id=} вызвал команду do_help')

    text = [
        f'Раздел <b>H E L P</b>',
        f'',
        f'Этот <b>бот</b> сделан пользователем (weldoy)',
        f'Если кому-то интересно, вот мой <a href="github.com/weldoy">GitHub</a> :3',
        f'Предназначен для развлечений :)',
        f'Чтобы узнать <b>полный функционал</b>, напишите /menu'
    ]
    text = '\n'.join(text)

    update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


if __name__ == '__main__':
    main()
