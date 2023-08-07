from PIL import Image
import numpy as np
from math import floor


ASCII_TAPE = ' .,:;i1tfLCG08@'


def image_to_matrix(image: Image) -> np.array:
    image = image.convert('L')
    array = np.array(image)
    return array / 256.0


def mean_to_ascii(mean: float) -> str:
    index = floor(mean * len(ASCII_TAPE))
    symbol = ASCII_TAPE[index]
    return symbol


def transform(image: Image, out_width: int, out_height: int) -> str:
    width, height = image.size
    frame_width = width // out_width
    frame_height = height // out_height
    matrix = image_to_matrix(image)
    lines = []
    for row in range(0, height, frame_height):
        line = ''
        for col in range(0, width, frame_width):
            extracted_frame = matrix[row:row + frame_height, col:col + frame_width]
            mean_value = extracted_frame.mean()
            ascii_value = mean_to_ascii(mean_value)
            line += ascii_value
        lines.append(line)
    output = '\n'.join(lines)
    return output
