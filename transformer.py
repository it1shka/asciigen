from PIL import Image
import numpy as np
from math import floor


class Transformer:
    def __init__(self, ascii_tape: str, frame_width: int, frame_height: int) -> None:
        self.ascii_tape = ascii_tape
        self.frame_width = frame_width
        self.frame_height = frame_height

    @staticmethod
    def image_to_matrix(image: Image) -> np.array:
        image = image.convert('L')
        array = np.array(image)
        return array / 256.0

    def mean_to_ascii(self, mean: float) -> str:
        index = floor(mean * len(self.ascii_tape))
        ascii = self.ascii_tape[index]
        return ascii

    def apply(self, image: Image) -> str:
        width, height = image.size
        matrix = self.image_to_matrix(image)
        lines = []
        for row in range(0, height, self.frame_height):
            line = ''
            for col in range(0, width, self.frame_width):
                extracted_frame = matrix[row:row + self.frame_height, col:col + self.frame_width]
                mean_value = extracted_frame.mean()
                ascii_value = self.mean_to_ascii(mean_value)
                line += ascii_value
            lines.append(line)
        output = '\n'.join(lines)
        return output
