from datetime import datetime

# Dữ liệu mẫu cho "Xổ số" (chuỗi số ngẫu nhiên 0-9)
SAMPLE_SOSO_PATTERNS = [
    ("1 2 3 4 5 6 7 8 9 0", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("9 8 7 6 5 4 3 2 1 0", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("0 1 2 3 4 5 6 7 8 9", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    ("5 5 5 4 4 3 3 2 2 1", "number", datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
]

def get_soso_patterns():
    return [pattern[0] for pattern in SAMPLE_SOSO_PATTERNS]