# sample_data.py
from datetime import datetime

# Dữ liệu mẫu cho kq_patterns
SAMPLE_PATTERNS = [
    # Mẫu 1-30: Dạng C/L (letter)
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

    # Mẫu 1-10: Dạng số (number) - đã mã hóa
    ("2222432302222322230232211442241023122101232133", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("3131323312222232211324133223132323130322111132022221", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("032223011024322230243223221311222133031233030233111333", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("223213213324034431222120243232422131021432221013321023", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("323211311214141233112123113423213233111221323123313", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("222331313112221222323120221232111222222221222012333", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("231332111221322313221114210133231312222131302312011", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1312124122323421131231131311222123123330123121132121", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1201212212312101203231211321120321421242213231012123", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1210133403300330232231332333321331222332224223434221", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("1122232133342141042311223111332323113322331032332102", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("241331102433111332311131131213224233342432222413210121", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("222311213410114033112312223201231321111211321211231321", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("231242112132211431211433122120322343122342423231242", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("2232133111332302440203331123413234133232133313222333", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
]

def get_sample_patterns():
    return SAMPLE_PATTERNS