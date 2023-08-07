import sys
from textwrap import dedent
from PIL import Image
from lib import transform
from math import floor


SIZE_COMPRESSION = 12


def start_console_application() -> None:
    print(dedent('''
        You entered application mode of asciigen.
        
        Now you will be asked to prompt image paths 
        to convert those images to ascii art.
        
        The input has a format:
        <image-path> width:<output-width> height:<output-height> file:<output-file>
        
        To exit the application, type "exit".
    '''))
    index = 1
    while True:
        raw_input = input(f'({index})> ')
        index += 1
        input_tokens = raw_input.strip().split()
        if not input_tokens:
            print('No input provided. ')
            continue

        start_token, rest_tokens = input_tokens[0], input_tokens[1:]
        if start_token == 'exit':
            print('Exiting the application. ')
            return

        try:
            image = Image.open(start_token)
        except FileNotFoundError:
            print(f'Image "{start_token}" does not exist. ')
            continue

        params = tokens_to_dict(rest_tokens)
        out_width, out_height = get_ascii_size(image, params)
        ascii_output = transform(image, out_width, out_height)
        print(ascii_output)

        if 'file' not in params:
            continue
        output_file_path = params['file']
        with open(output_file_path, 'w+') as output_file:
            output_file.write(ascii_output)


def get_ascii_size(image: Image, params: dict[str, str]) -> tuple[int, int]:
    img_width, img_height = image.size
    width, height = params.get('width'), params.get('height')
    if width:
        width = int(width)
    if height:
        height = int(height)
    if not width and not height:
        width, height = img_width // SIZE_COMPRESSION, img_height // SIZE_COMPRESSION
    if not width:
        width = floor(img_width * (height / img_height))
    if not height:
        height = floor(img_height * (width / img_width))
    return width, height


def tokens_to_dict(tokens: list[str]) -> dict[str, str]:
    output = dict()
    for token in tokens:
        parts = token.split(':')
        if len(parts) != 2:
            print(f'Wrong format of argument: {token}. ')
            continue
        key, value = parts
        output[key] = value
    return output


def start_telegram_bot() -> None:
    print(dedent('''
        You entered telegram bot mode of asciigen.
        
        Hit Ctrl+C or Ctrl+D to stop it.
    '''))
    print('TODO: This is incomplete')
    sys.exit(1)
    # TODO: ...


def get_mode() -> str:
    if len(sys.argv) < 2:
        output = input('Please, provide a mode (app/bot): ')
        output = output.strip()
    else:
        output = sys.argv[1]
    return output


if __name__ == '__main__':
    mode = get_mode()
    if mode == 'app':
        start_console_application()
    elif mode == 'bot':
        start_telegram_bot()
    else:
        print(f'Unknown mode: {mode}')
        sys.exit(1)
