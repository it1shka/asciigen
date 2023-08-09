from textwrap import dedent
import sys
import telebot as tg
from telebot.types import *
from PIL import Image
from io import BytesIO
import requests
from lib import transform
from typing import Any


TG_SIZE_COMPRESSION = 25


def any_nonempty(*args: Any) -> Any:
    for each in args:
        if each is not None:
            return each
    return None


def parse_env_file(envpath: str = '.env') -> None:
    with open(envpath, 'r') as envfile:
        for line in envfile.readlines():
            pair = line.split('=')
            if len(pair) != 2:
                print(f'Failed to parse env file: {line}')
                continue
            key, value = map(lambda e: e.strip(), pair)
            os.environ[key] = value


def load_welcome_cat() -> str:
    try:
        with open('cat.txt', 'r') as file:
            contents = file.read()
            return contents
    except FileNotFoundError:
        return 'Failed to get welcome cat :('


def wrapped(ascii_message: str, title: str = 'Result') -> str:
    return f'{title}: \n\n```\n{ascii_message}\n```'


def setup_bot(tgbot: tg.TeleBot) -> None:
    @tgbot.message_handler(commands=['start'])
    def welcome(message: Message) -> None:
        chat_id = message.chat.id
        try:
            user_name = message.from_user.first_name
            tgbot.send_message(chat_id, dedent(f'''
                **Hello and welcome, {user_name}**
                
                This bot will help you turn images into
                their ascii representation
                
                **Just attach an image**
                 
                Additionally, in caption you can specify
                width and height of the output in the form:
                
                **Width x Height**
            '''))
            welcome_cat = wrapped(load_welcome_cat(), 'Example (a cute cat)')
            tgbot.send_message(chat_id, welcome_cat)
        except Exception:
            tgbot.send_message(chat_id, 'Internal error happened :(')

    @tgbot.message_handler(content_types=['photo'])
    def ascii_transform(message: Message) -> None:
        chat_id = message.chat.id
        try:
            photo_id = message.photo[-1].file_id
            photo_path = tgbot.get_file(photo_id).file_path

            image_url = f"https://api.telegram.org/file/bot{os.environ['TOKEN']}/{photo_path}"
            response = requests.get(image_url)
            image_content = response.content
            image = Image.open(BytesIO(image_content))

            text = any_nonempty(message.caption, message.text, '')
            params = text.split('x')
            if len(params) != 2:
                width, height = 30, 20
            else:
                width, height = map(lambda e: int(e.strip()), params)
            ascii_text = transform(image, width, height)
            ascii_text = wrapped(ascii_text)

            tgbot.send_message(chat_id, ascii_text)
        except Exception:
            tgbot.send_message(chat_id, 'Internal error happened :(')


if __name__ == '__main__':
    print(dedent('''
        You entered telegram bot version of this application.
        
        Press Ctrl+C or Ctrl+D multiple times to exit.
    '''))

    parse_env_file()

    if 'TOKEN' not in os.environ:
        print('Failed to get Telegram token. ')
        sys.exit(1)
    token = os.environ['TOKEN']

    bot = tg.TeleBot(token, parse_mode='Markdown')
    setup_bot(bot)
    bot.polling()
