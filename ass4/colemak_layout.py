# QWERTY Keyboard layout data

keys = {
    # Number row
    '`': {'pos': (0, 4), 'start': 'a'},
    '1': {'pos': (1, 4), 'start': 'a'},
    '2': {'pos': (2, 4), 'start': 'a'},
    '3': {'pos': (3, 4), 'start': 's'},
    '4': {'pos': (4, 4), 'start': 'd'},
    '5': {'pos': (5, 4), 'start': 'f'},
    '6': {'pos': (6, 4), 'start': 'j'},
    '7': {'pos': (7, 4), 'start': 'j'},
    '8': {'pos': (8, 4), 'start': 'k'},
    '9': {'pos': (9, 4), 'start': 'l'},
    '0': {'pos': (10, 4), 'start': ';'},
    '-': {'pos': (11, 4), 'start': ';'},
    '=': {'pos': (12, 4), 'start': ';'},
    
    # Top letter row
    'q': {'pos': (1.5, 3), 'start': 'a'},
    'w': {'pos': (2.5, 3), 'start': 'r'},
    'f': {'pos': (3.5, 3), 'start': 's'},
    'p': {'pos': (4.5, 3), 'start': 't'},
    'g': {'pos': (5.5, 3), 'start': 't'},
    'j': {'pos': (6.5, 3), 'start': 'n'},
    'l': {'pos': (7.5, 3), 'start': 'n'},
    'u': {'pos': (8.5, 3), 'start': 'e'},
    'y': {'pos': (9.5, 3), 'start': 'i'},
    ';': {'pos': (10.5, 3), 'start': 'o'},
    '[': {'pos': (11.5, 3), 'start': 'o'},
    ']': {'pos': (12.5, 3), 'start': 'o'},
    '\\': {'pos': (13.5, 3), 'start': 'o'},
    
    # Home row
    'a': {'pos': (1.75, 2), 'start': 'a'},
    'r': {'pos': (2.75, 2), 'start': 'r'},
    's': {'pos': (3.75, 2), 'start': 's'},
    't': {'pos': (4.75, 2), 'start': 't'},
    'd': {'pos': (5.75, 2), 'start': 't'},
    'h': {'pos': (6.75, 2), 'start': 'n'},
    'n': {'pos': (7.75, 2), 'start': 'n'},
    'e': {'pos': (8.75, 2), 'start': 'e'},
    'i': {'pos': (9.75, 2), 'start': 'i'},
    'o': {'pos': (10.75, 2), 'start': 'o'},
    "'": {'pos': (11.75, 2), 'start': 'o'},
    
    # Bottom letter row
    'z': {'pos': (2.25, 1), 'start': 'a'},
    'x': {'pos': (3.25, 1), 'start': 'r'},
    'c': {'pos': (4.25, 1), 'start': 's'},
    'v': {'pos': (5.25, 1), 'start': 't'},
    'b': {'pos': (6.25, 1), 'start': 't'},
    'k': {'pos': (7.25, 1), 'start': 'n'},
    'm': {'pos': (8.25, 1), 'start': 'n'},
    ',': {'pos': (9.25, 1), 'start': 'e'},
    '.': {'pos': (10.25, 1), 'start': 'i'},
    '/': {'pos': (11.25, 1), 'start': 'o'},
    
    # Special keys
    'Shift_L': {'pos': (0, 1), 'start': 'a'},
    'Shift_R': {'pos': (12.25, 1), 'start': ';'},
    'Ctrl_L': {'pos': (0, 0), 'start': 'a'},
    'Alt_L': {'pos': (2, 0), 'start': 'a'},
    'Space': {'pos': (5, 0), 'start': 'f'},
    'Alt_R': {'pos': (8, 0), 'start': 'j'},
    'Ctrl_R': {'pos': (10, 0), 'start': ';'},
}

characters = {
    # Lowercase letters (unchanged)
    'a': ('a',), 'b': ('b',), 'c': ('c',), 'd': ('d',), 'e': ('e',),
    'f': ('f',), 'g': ('g',), 'h': ('h',), 'i': ('i',), 'j': ('j',),
    'k': ('k',), 'l': ('l',), 'm': ('m',), 'n': ('n',), 'o': ('o',),
    'p': ('p',), 'q': ('q',), 'r': ('r',), 's': ('s',), 't': ('t',),
    'u': ('u',), 'v': ('v',), 'w': ('w',), 'x': ('x',), 'y': ('y',),
    'z': ('z',),
    
    # Uppercase letters (updated)
    'A': ('Shift_R', 'a'), 'B': ('Shift_R', 'b'), 'C': ('Shift_R', 'c'),
    'D': ('Shift_R', 'd'), 'E': ('Shift_R', 'e'), 'F': ('Shift_R', 'f'),
    'G': ('Shift_R', 'g'), 'H': ('Shift_L', 'h'), 'I': ('Shift_L', 'i'),
    'J': ('Shift_L', 'j'), 'K': ('Shift_L', 'k'), 'L': ('Shift_L', 'l'),
    'M': ('Shift_L', 'm'), 'N': ('Shift_L', 'n'), 'O': ('Shift_L', 'o'),
    'P': ('Shift_L', 'p'), 'Q': ('Shift_R', 'q'), 'R': ('Shift_R', 'r'),
    'S': ('Shift_R', 's'), 'T': ('Shift_R', 't'), 'U': ('Shift_L', 'u'),
    'V': ('Shift_R', 'v'), 'W': ('Shift_R', 'w'), 'X': ('Shift_R', 'x'),
    'Y': ('Shift_L', 'y'), 'Z': ('Shift_R', 'z'),
    
    # Numbers and their shifted symbols (updated)
    '1': ('1',), '!': ('Shift_R', '1'),
    '2': ('2',), '@': ('Shift_R', '2'),
    '3': ('3',), '#': ('Shift_R', '3'),
    '4': ('4',), '$': ('Shift_R', '4'),
    '5': ('5',), '%': ('Shift_R', '5'),
    '6': ('6',), '^': ('Shift_L', '6'),
    '7': ('7',), '&': ('Shift_L', '7'),
    '8': ('8',), '*': ('Shift_L', '8'),
    '9': ('9',), '(': ('Shift_L', '9'),
    '0': ('0',), ')': ('Shift_L', '0'),
    
    # Other symbols (updated)
    '`': ('`',), '~': ('Shift_R', '`'),
    '-': ('-',), '_': ('Shift_L', '-'),
    '=': ('=',), '+': ('Shift_L', '='),
    '[': ('[',), '{': ('Shift_L', '['),
    ']': (']',), '}': ('Shift_L', ']'),
    '\\': ('\\',), '|': ('Shift_L', '\\'),
    ';': (';',), ':': ('Shift_L', ';'),
    "'": ("'",), '"': ('Shift_L', "'"),
    ',': (',',), '<': ('Shift_L', ','),
    '.': ('.',), '>': ('Shift_L', '.'),
    '/': ('/',), '?': ('Shift_L', '/'),
    
    # Space (unchanged)
    ' ': ('Space',),
}