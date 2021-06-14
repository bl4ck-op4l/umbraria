from cv2 import cv2
import json
import os.path as path

_alphabet = None
def get_alphabet():
    global _alphabet
    if _alphabet is not None:
        return _alphabet

    _alphabet = Alphabet()
    return _alphabet


class Alphabet:
    def __init__(self):
        with open('alphabet/letters.json', 'r') as f:
            self.data = json.load(f)

        self._alph = [Letter(item) for item in self.data.items()]

    def __iter__(self):
        return iter(self._alph)


class Letter:
    def __init__(self, item):
        self.char = item[0]
        self.image_path = path.join('alphabet', item[1])
        self.image = cv2.imread(path.join('alphabet', item[1]), cv2.IMREAD_GRAYSCALE)

        if self.image is None:
            raise Exception('Image not found!')

        self.plain = self.char
        if self.plain == '█':
            self.plain = '?'
        self.threshold = .855
        if self.char == ' ':
            self.threshold = .7 
        elif self.char == 'd':
            self.threshold = .875
        elif self.char == ',':
            self.threshold = .86

