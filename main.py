import sys
from textwrap import dedent
from PIL import Image
from transformer import Transformer


FRAME_WIDTH = 3
FRAME_HEIGHT = 3
ASCII_TAPE = ' .,:;ox%#@'


def application() -> None:
    print(dedent('''
        You entered application mode of asciigen.
        
        Now you will be asked to prompt image paths 
        to convert those images to ascii art.
        
        To exit the application, type "exit".
    '''))
    index = 1
    transformer = Transformer(ASCII_TAPE, FRAME_WIDTH, FRAME_HEIGHT)
    while True:
        user_input = input(f'({index})> ')
        if user_input == 'exit':
            return
        try:
            image = Image.open(user_input)
            ascii = transformer.apply(image)
            print(ascii)
        except FileNotFoundError:
            print('File does not exist')


def telegram_bot() -> None:
    print(dedent('''
        You entered telegram bot mode of asciigen.
        
        Hit Ctrl+C or Ctrl+D.
    '''))
    print('TODO: This is incomplete')
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        mode = input('Please, provide a mode (app/bot): ')
    else:
        mode = sys.argv[1]
    if mode == 'app':
        application()
    elif mode == 'bot':
        telegram_bot()
    else:
        print(f'Unknown mode: {mode}')
        sys.exit(1)
