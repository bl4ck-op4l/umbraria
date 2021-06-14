import json
import string
from pathlib import Path

class Decryptor:
    def __init__(self, type_, text):
        self._type = type_
        self._text = text
        self._get_info()
        self._decrypt()
    
    def _get_info(self):
        path = Path('codes.json')
        if path.is_file():
            data = None
            with path.open('r') as f:
                data = json.load(f)
            if self._type in data:
                self.key = data[self._type]['key']
                if self.key is not None:
                    self.fields = data[self._type]['fields']
                else:
                    self.fields = None
            else:
                self.key = None
                self.fields = None
        else:
            self.key = None
            self.fields = None
    
    def _decrypt(self):
        if self.key is None:
            self.plaintext = self._text
            return
        
        lines = self._text.split('\n')
        res = []
        if self.fields is None:
            self.fields = []
            for line in lines:
                idx = line.index(' ')
                self.fields.append(line[:idx])
                res.append(line[:idx] + _vigenere(line[idx:], self.key))
        else:
            if len(lines) != len(self.fields):
                raise Exception('Document has incorrect format: lines count')

            for line, name in zip(lines, self.fields):
                pos = len(name)
                prefix = name
                if not line.startswith(name):
                    # raise Exception(f'Document has incorrect format: no field "{name}"')
                    pos = line.index(' ')
                    prefix = line[:pos]
                res.append(prefix + ' ' + _vigenere(line[pos:].strip(), self.key))

        self.plaintext = '\n'.join(res)

        
def _vigenere(text, key):
    res = ''
    i = 0
    alph = string.ascii_lowercase
    for letter in text:
        if letter == '█':
            res += letter
            i = (i + 1) % len(key)
            continue

        if letter.isalpha():
            key_idx = alph.index(key[i])
            i = (i + 1) % len(key)
            res += alph[(alph.index(letter) - key_idx) % 26]
        else:
            res += letter
    return res
        