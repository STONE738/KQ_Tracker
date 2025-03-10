from flask import Flask, render_template, request, session
import json
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Cần thiết để sử dụng session

# Đường dẫn đến file database
DATABASE_FILE = 'database.json'
HISTORY_FILE = 'history.json'

# Biến toàn cục để lưu trữ trạng thái
current_kq = ""
last_prediction = None
win_count = 0
lose_count = 0
win_streak = 0
lose_streak = 0
max_win_streak = 0
max_lose_streak = 0

# Tải dữ liệu từ database
def load_database():
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('kq_patterns', [])
    return []

# Lưu dữ liệu vào database
def save_database(kq_patterns):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump({'kq_patterns': kq_patterns}, f, ensure_ascii=False, indent=2)

# Tải dữ liệu từ history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data.get('highest_win_streak', 0), data.get('highest_lose_streak', 0)
    return 0, 0

# Lưu dữ liệu vào history
def save_history(highest_win_streak, highest_lose_streak):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            'highest_win_streak': highest_win_streak,
            'highest_lose_streak': highest_lose_streak
        }, f, ensure_ascii=False, indent=2)

# Hàm xử lý chuỗi KQ
def process_kq(kq_input):
    kq_input = kq_input.upper().replace(" ", "")
    kq_list = list(kq_input)
    kq_list = [x for x in kq_list if x in ['C', 'L']]
    return kq_list

# Hàm phân tích KQ cho một mẫu cụ thể
def analyze_single_kq(kq_list, kq_length, recent_kq):
    patterns = {}
    for i in range(len(kq_list) - kq_length):
        pattern = tuple(kq_list[i:i + kq_length])
        next_result = kq_list[i + kq_length] if i + kq_length < len(kq_list) else None
        if next_result:
            if pattern in patterns:
                patterns[pattern].append(next_result)
            else:
                patterns[pattern] = [next_result]

    current_pattern = tuple(recent_kq)
    if current_pattern in patterns:
        next_results = patterns[current_pattern]
        total_matches = len(next_results)
        c_count = next_results.count('C')
        l_count = next_results.count('L')
        return {
            'total_matches': total_matches,
            'c_count': c_count,
            'l_count': l_count
        }
    return None

# Hàm phân tích tổng hợp từ nhiều mẫu
def analyze_kq(kq_list, kq_length, db_kq_patterns):
    global last_prediction
    if not kq_list and not db_kq_patterns:
        return {'error': 'Không có dữ liệu để phân tích.'}

    recent_kq = kq_list[-kq_length:] if len(kq_list) >= kq_length else None
    if not recent_kq:
        return {'error': f'Chuỗi KQ chưa đủ {kq_length} kết quả để phân tích.'}

    total_matches = 0
    total_c_count = 0
    total_l_count = 0

    if len(kq_list) >= kq_length:
        user_result = analyze_single_kq(kq_list, kq_length, recent_kq)
        if user_result:
            total_matches += user_result['total_matches']
            total_c_count += user_result['c_count']
            total_l_count += user_result['l_count']

    for pattern in db_kq_patterns:
        pattern_list = process_kq(pattern)
        if len(pattern_list) >= kq_length:
            db_result = analyze_single_kq(pattern_list, kq_length, recent_kq)
            if db_result:
                total_matches += db_result['total_matches']
                total_c_count += db_result['c_count']
                total_l_count += db_result['l_count']

    if total_matches == 0:
        return {'error': 'Không tìm thấy mẫu phù hợp để dự đoán.'}

    c_percentage = (total_c_count / total_matches) * 100 if total_matches > 0 else 50
    l_percentage = (total_l_count / total_matches) * 100 if total_matches > 0 else 50
    prediction = 'C' if c_percentage > l_percentage else 'L'
    last_prediction = prediction

    return {
        'prediction': prediction,
        'total_matches': total_matches,
        'c_percentage': round(c_percentage, 2),
        'l_percentage': round(l_percentage, 2)
    }

# Route chính
@app.route('/', methods=['GET', 'POST'])
def index():
    global current_kq, last_prediction, win_count, lose_count, win_streak, lose_streak, max_win_streak, max_lose_streak

    # Khởi tạo trạng thái nếu chưa có
    if 'state' not in session:
        session['state'] = 'phan_tich'  # Mặc định hiển thị dòng "Phân Tích"

    result = None
    selected_kq_length = 4
    update_kq_length = 4
    real_kq_input = ""
    db_kq_patterns = load_database()

    # Tải dữ liệu lịch sử
    highest_win_streak, highest_lose_streak = load_history()

    if request.method == 'POST':
        if 'new_game' in request.form:
            current_kq = ""
            last_prediction = None
            win_count = 0
            lose_count = 0
            win_streak = 0
            lose_streak = 0
            max_win_streak = 0
            max_lose_streak = 0
            session['state'] = 'phan_tich'  # Reset về trạng thái "Phân Tích"
            return render_template('index.html', current_kq=current_kq, selected_kq_length=selected_kq_length, update_kq_length=update_kq_length, real_kq_input=real_kq_input, win_count=win_count, lose_count=lose_count, win_streak=win_streak, lose_streak=lose_streak, max_win_streak=max_win_streak, max_lose_streak=max_lose_streak, highest_win_streak=highest_win_streak, highest_lose_streak=highest_lose_streak, state=session['state'])

        kq_input = request.form.get('kq_input', '')
        selected_kq_length = int(request.form.get('kq_length', 4))
        if kq_input:
            kq_list = process_kq(kq_input)
            if kq_list:
                current_kq = " ".join(kq_list)
                new_pattern = " ".join(kq_list)
                if new_pattern not in db_kq_patterns:
                    db_kq_patterns.append(new_pattern)
                    save_database(db_kq_patterns)
                result = analyze_kq(kq_list, selected_kq_length, db_kq_patterns)
                if not result.get('error'):  # Nếu phân tích thành công (không có lỗi)
                    session['state'] = 'cap_nhat'  # Chuyển sang trạng thái "Cập Nhật"

        real_kq_input = request.form.get('real_kq_input', '')
        update_kq_length = int(request.form.get('update_kq_length', 4))
        if real_kq_input:
            real_kq_list = process_kq(real_kq_input)
            if real_kq_list:
                current_kq_list = current_kq.split() if current_kq else []
                current_kq_list.extend(real_kq_list)
                current_kq = " ".join(current_kq_list)

                new_pattern = " ".join(real_kq_list)
                if new_pattern not in db_kq_patterns:
                    db_kq_patterns.append(new_pattern)
                    save_database(db_kq_patterns)

                if last_prediction and real_kq_list:
                    actual_result = real_kq_list[-1]
                    if actual_result == last_prediction:
                        win_count += 1
                        win_streak += 1
                        lose_streak = 0
                        max_win_streak = max(max_win_streak, win_streak)
                    else:
                        lose_count += 1
                        lose_streak += 1
                        win_streak = 0
                        max_lose_streak = max(max_lose_streak, lose_streak)

                    # Cập nhật lịch sử nếu cần
                    if max_win_streak > highest_win_streak:
                        highest_win_streak = max_win_streak
                    if max_lose_streak > highest_lose_streak:
                        highest_lose_streak = max_lose_streak
                    save_history(highest_win_streak, highest_lose_streak)

                result = analyze_kq(current_kq_list, update_kq_length, db_kq_patterns)

    return render_template('index.html', current_kq=current_kq, result=result, selected_kq_length=selected_kq_length, update_kq_length=update_kq_length, real_kq_input=real_kq_input, win_count=win_count, lose_count=lose_count, win_streak=win_streak, lose_streak=lose_streak, max_win_streak=max_win_streak, max_lose_streak=max_lose_streak, highest_win_streak=highest_win_streak, highest_lose_streak=highest_lose_streak, state=session['state'])

if __name__ == '__main__':
    app.run(debug=True)