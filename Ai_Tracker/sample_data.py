from datetime import datetime

SAMPLE_PATTERNS = [
    ("C C C C C L C L C C C C C L C C C L C C L C C L L C C C C C L C C L L C C L C L C L C L L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L L L L C L L L C C C C C L C C L L L C C L L L C C L L L C L C L L L C L C C L L L L L C C C C C C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L C C C L C L L C C C L C C C L C C C L C C L C C L L L L C C C L L L C L L C L L C L C C L L L L L L L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L C L L C L L L C C C L C C L L C C C L C C C C L C L C C C C L L L C C L C L C C C L C L L L C L C C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C L C L L L L L C L C L C L C L L L L C L C L L L L C C L C L L C L L L L L C C L L C L L C L L L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C C L L L L L L L L C C C L C C C L C L L C C C C L C L C L L L C C C C C C C C L C C C C L C L L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L L L L C L L L C C L L C C L L L C C L L L C C L C L L L C L L L L C C C C L L L L C C L L C C L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L L C L C C L C C L C L C C L L L L C L L L L L L L L C C C L C L L C L L L C L C L L C L L L C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C C L C L C C L C L L C L C L C C L C L L C L L L C L L C C L C L C C L C C C C L L C L L C L C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C L C L L L C C L L C C L L C C L C C L L L L C L L L L C L L L L C C C L C C C C C C L C L C C C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L L L L L L L C C C L C C C L C L L C C C C L C L C L L L C C C C C C C C L C C C C L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L L L L C L L L L C C L L C C L L L C C L L L C C L C L L L C L L L L C C C C L L L L C C L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L C L C C L C C L L L C C C C L C L C L L C L L C L L L C L L C C C C L L L C L L L L L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L C C C L C L L L L C C C C C L L C L C C L C L C C L L C C L L L C C C L C C C C C L L C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C L C L L L C C L L C C L L C C L C C L L L L C L L L L C L L L L C C C L L C C C C C C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C C C L C C C L C C L C L C C C C C L L C L L L C C C C C C L C C C L L L L L C L L C L L L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L L C C L L C L L C L L C L C L L L C C L C L C C C L C C C L C C L C L L C C C L C L C C C C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C C C L L C L L C L L C C L L L L L C C L C C L C C L L C C C L C C C C C L C L C C C C L C C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C C L L C L L C C L C C L L C L L L C C C L C L L C C C L L C L C C L L C L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L L C C L C C L L C L L C C C L C L L C C L C L C C L L C C L C L L C L C C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L C L L C C L C L C C L L L C L C C L C L L C C C L L C L C C L L C L L C C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L C C L C L C C L L C C L C L C L L C C L C C L L C L C C L L C C L C L C L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L C L C C L L C C C L C L L C L C C L L C C L C L C L C C L L C L C C L C L L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C L C C L C L L C C C L C L C L C C L L C L C C L C L L C C L C L C C L L C C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L L C L C C L C L L C C C L C L C L L C C L C C L L C C L C L C L C C L L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L C L C C L C L C C L L C C C L C L L C C L C L C L C C L L C C L C L C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C L C C L L C C L C L C L C C L L C C L C L C L C C L L C C L C L C C L L C L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L C L C C L L C C L C L C C L L C C L C L C L L C C C L C L C L C C L L C L C C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("C C L C L C L C C L L C C L C L C L L C C L C C L C L C L C C L L C C L C L C L", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("L L C C L C L C C L C L L C C C L C L C L C C L L C C L C L C L C C L L C C L C", "letter", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("3131323312222232211324133223132323130322111132022221", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("032223011024322230243223221311222133031233030233111333", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("223213213324034431222120243232422131021432221013321023", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("323211311214141233112123113423213233111221323123313", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("222331313112221222323120221232111222222221222012333", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("231332111221322313221114210133231312222131302312011", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1312124122323421131231131311222123123330123121132121", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1201212212312101203231211321120321421242213231012123", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1210133403300330232231332333321331222332224223434221", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1122232133342141042311223111332323113322331032332102", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
]

def get_sample_patterns():
    return SAMPLE_PATTERNS

def decode_number_pattern(encoded_pattern):
    return " ".join(char for char in encoded_pattern if char in ['0', '1', '2', '3', '4'])

def get_letter_patterns():
    return [pattern[0] for pattern in SAMPLE_PATTERNS if pattern[1] == "letter"]

def get_number_patterns():
    return [decode_number_pattern(pattern[0]) for pattern in SAMPLE_PATTERNS if pattern[1] == "number"]