import math
from cv2 import cv2
import numpy as np
import letters
from texter import Texter

class Extractor:
    def __init__(self, path):
        self._path = path
        self._image = cv2.imread(path)
        self._convert_image()
        self._extract_letters()
        self._remove_near()

    def _convert_image(self):
        self._image = cv2.cvtColor(self._image, cv2.COLOR_BGR2GRAY)
        self._image = cv2.threshold(self._image, 100, 255, cv2.THRESH_BINARY)[1]

    def _extract_letters(self):
        self._found_letters = []
        for letter in letters.get_alphabet():
            found = self._search_template(letter.image, letter.threshold)
            self._found_letters += _add_letter(found, letter)

    def _search_template(self, template, threshold):
        res = cv2.matchTemplate(self._image, template, cv2.TM_CCOEFF_NORMED)
        return map(lambda x: (*x, res[x[1],x[0]]), zip(*np.where(res >= threshold)[::-1]))

    def _remove_near(self):
        res = []
        for let1 in self._found_letters:
            for i in range(len(res)):
                let2 = res[i]
                if math.dist(let1[:2], let2[:2]) < 10:
                    if let2[2] < let1[2]:
                        res[i] = let1
                    break
            else:
                res.append(let1)
        self._found_letters = res

    def get_text(self, correct_lines=True):
        self._texter = Texter(self._found_letters)
        return self._texter.get_text(correct_lines)

    def save_parsed(self, path):
        image = cv2.imread(self._path)
        for line in self._texter.get_lines():
            for letter in line:
                h, w = letter[3].image.shape
                cv2.rectangle(image, letter[:2], (letter[0] + w, letter[1] + h), (0,0,255), 2)
                cv2.putText(
                    image, letter[3].plain, (letter[0] + 5, letter[1] + 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),
                    2, cv2.LINE_AA
                )
        
        if hasattr(self, '_texter'):
            w = image.shape[1]
            bounds = self._texter.get_line_bounds()
            for bound in bounds:
                cv2.line(image, (0, bound[0]), (w, bound[0]), (255,0,0), 2)
                cv2.line(image, (0, bound[1]), (w, bound[1]), (255,0,0), 2)

        cv2.imwrite(path, image)

def _add_letter(points, letter):
    return list(map(lambda x: (*x, letter), points))
