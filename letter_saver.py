from cv2 import cv2

img = cv2.imread("posts/post2.jpg")
letter = img[490:560, 305:353]
char = '#'
grayletter = cv2.threshold(cv2.cvtColor(letter, cv2.COLOR_BGR2GRAY), 100, 255, cv2.THRESH_BINARY)[1]
# cv2.imshow("Umbraria", grayletter)
# cv2.waitKey(0)
import json
d = None
with open('alphabet/letters.json', 'r') as f:
    d = json.load(f)

import re
if re.match(r'[a-z]', char):
    d[char] = f'{char}.jpg'
else:
    d[char] = f'_{ord(char)}.jpg'

cv2.imwrite(f'alphabet/{d[char]}', grayletter)
with open('alphabet/letters.json', 'w') as f:
    json.dump(d, f)