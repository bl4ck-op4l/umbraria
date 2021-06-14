import re
from pyzbar import pyzbar
from PIL import Image
from extractor import Extractor
from decryptor import Decryptor

class Document:
    def __init__(self, path):
        self._path = path
        self._image = Image.open(path)
        self._codes = pyzbar.decode(self._image)
        self._parse_type()
        self._parse_image()
        self._decrypt()

    def _parse_type(self):
        for code in self._codes:
            match = re.match(rb'^([a-z]{3})(\d{3})$', code.data)
            if not match:
                continue

            self.type = match.group(1).decode()
            self.number = int(match.group(2).decode())
            break

    def _parse_image(self):
        self._extractor = Extractor(self._path)
        self.text = self._extractor.get_text()

    def _decrypt(self):
        self._decryptor = Decryptor(self.type, self.text)
        self.plaintext = self._decryptor.plaintext

    def print(self):
        YELLOW = '\x1b[1;93m'
        WHITE = '\x1b[0m'
        print(f'{YELLOW}Type:{WHITE} {self.type}')
        print(f'{YELLOW}Number:{WHITE} {self.number:03}')
        if self._decryptor.key is None:
            print(f'{YELLOW}Key:{WHITE} Unknown')
        else:
            print(f'{YELLOW}Key:{WHITE} {self._decryptor.key}')
        print(f'{YELLOW}Text:{WHITE}\n{self.text}')
        if self.plaintext != self.text:
            print(f'{YELLOW}Decrypted:{WHITE}\n{self.plaintext}')

    def save_parsed_image(self, path):
        self._extractor.save_parsed(path)


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} files...')
        exit(1)

    for fname in sys.argv[1:]:
        d = Document(fname)
        d.print()
        d.save_parsed_image('newres.jpg')
