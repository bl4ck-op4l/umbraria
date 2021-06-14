class Texter:
    LINE_WINDOW_HEIGHT = 13

    def __init__(self, letters):
        self._letters = letters
        self._group_by_lines()
        self._remove_ghost_lines()
        self._sort_lines()

    def _group_by_lines(self):
        lines = dict()
        for letter in self._letters:
            for line in lines:
                if abs(letter[1]-line) < self.LINE_WINDOW_HEIGHT:
                    lines[line].append(letter)
                    break
            else:
                lines[letter[1]] = [letter]

        self._lines = lines
    
    def _remove_ghost_lines(self):
        positions = sorted(self._lines.keys())
        for p1, p2 in zip(positions, positions[1:]):
            if p2 - p1 < self.LINE_WINDOW_HEIGHT * 2:
                if len(self._lines[p1]) < len(self._lines[p2]):
                    del self._lines[p1]
                else:
                    del self._lines[p2] 
        

    def _sort_lines(self):
        newlines = []
        for line in sorted(self._lines):
            newlines.append(sorted(self._lines[line]))
        self._positions = self._lines.keys()
        self._lines = newlines

    def get_text(self, correct_lines=True):
        lines = [''.join(map(lambda x: x[3].char, line)) for line in self._lines]

        if not correct_lines:
            return '\n'.join(lines)

        fixed = [lines[0]]
        for line in lines[1:]:
            if fixed[-1][-1] == ' ':
                fixed[-1] += line
            else:
                fixed.append(line)

        return _fix_numbers('\n'.join(fixed))
    
    def get_line_bounds(self):
        return map(lambda x: (x-self.LINE_WINDOW_HEIGHT, x+self.LINE_WINDOW_HEIGHT), self._positions)
    
    def get_lines(self):
        return self._lines

def _fix_numbers(text):
    import re
    alph = 'jabcdefghi'
    return re.sub(r'#([a-j])', lambda x: str(alph.index(x.group(1))), text)