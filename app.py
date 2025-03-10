from flask import Flask, render_template, request, session
import sqlite3
import json
import os
from datetime import datetime
from sample_data import get_sample_patterns

app = Flask(__name__)
app.secret_key = 'your-secret-key'

DATABASE = 'kq2_tracker.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS kq_patterns
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pattern TEXT NOT NULL,
                      format TEXT NOT NULL,
                      timestamp TEXT NOT NULL)''')  # Sửa NOT NOTNULL thành NOT NULL
        c.execute('''CREATE TABLE IF NOT EXISTS history
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      highest_win_streak INTEGER,
                      highest_lose_streak INTEGER,
                      timestamp TEXT NOT NULL)''')
        c.execute('''CREATE TABLE IF NOT EXISTS simulations
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      pattern TEXT NOT NULL,
                      result TEXT NOT NULL,
                      timestamp TEXT NOT NULL)''')
        
        c.execute("SELECT COUNT(*) FROM kq_patterns")
        if c.fetchone()[0] == 0:
            sample_patterns = get_sample_patterns()
            c.executemany("INSERT INTO kq_patterns (pattern, format, timestamp) VALUES (?, ?, ?)", sample_patterns)
        conn.commit()

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

current_kq = ""
last_prediction = None
win_count = 0
lose_count = 0
win_streak = 0
lose_streak = 0
max_win_streak = 0
max_lose_streak = 0

def standardize_kq(kq_input):
    kq_input = kq_input.upper().replace(" ", "")
    kq_list = list(kq_input)
    
    if all(x in ['0', '1', '2', '3', '4'] for x in kq_list):
        format_type = "number"
        kq_cl = ['C' if x in ['0', '2', '4'] else 'L' for x in kq_list]
    elif all(x in ['C', 'L'] for x in kq_list):
        format_type = "letter"
        kq_cl = kq_list
        kq_list = None
    else:
        return None, None, "Dữ liệu không hợp lệ (chỉ dùng 0-4 hoặc C/L)."
    
    return kq_list, kq_cl, format_type

def calculate_number_stats(kq_list, db_patterns):
    number_counts = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
    total_numbers = 0

    if kq_list:
        for num in kq_list:
            number_counts[num] += 1
            total_numbers += 1

    for pattern_row in db_patterns:
        pattern = pattern_row['pattern'].split()
        for num in pattern:
            if num in number_counts:
                number_counts[num] += 1
                total_numbers += 1

    number_percentages = {}
    for num in number_counts:
        number_percentages[num] = (number_counts[num] / total_numbers * 100) if total_numbers > 0 else 0
        number_percentages[num] = round(number_percentages[num], 2)

    return number_percentages

def analyze_single_kq(kq_cl, kq_length):
    patterns = {}
    for i in range(0, len(kq_cl) - kq_length, kq_length):
        pattern = tuple(kq_cl[i:i + kq_length])
        next_result = kq_cl[i + kq_length] if i + kq_length < len(kq_cl) else None
        if next_result:
            if pattern in patterns:
                patterns[pattern].append(next_result)
            else:
                patterns[pattern] = [next_result]
    return patterns

def analyze_kq(kq_input, kq_length, db_patterns, method="default"):
    global last_prediction
    kq_list, kq_cl, format_type = standardize_kq(kq_input)
    if not kq_cl:
        return {'error': format_type}

    if len(kq_cl) < kq_length:
        return {'error': f'KQ chưa đủ {kq_length} kết quả.'}

    total_matches = 0
    total_c_count = 0
    total_l_count = 0
    matched_patterns = set()

    recent_kq = kq_cl[-kq_length:] if len(kq_cl) >= kq_length else None
    if not recent_kq:
        return {'error': 'KQ không đủ dài.'}

    user_patterns = analyze_single_kq(kq_cl, kq_length)
    if tuple(recent_kq) in user_patterns:
        results = user_patterns[tuple(recent_kq)]
        pattern_key = (tuple(recent_kq), 'user')
        if pattern_key not in matched_patterns:
            total_matches += len(results)
            total_c_count += results.count('C')
            total_l_count += results.count('L')
            matched_patterns.add(pattern_key)

    for pattern_row in db_patterns:
        pattern = pattern_row['pattern'].split()
        pattern_kq_list, pattern_kq_cl, _ = standardize_kq("".join(pattern))
        if pattern_kq_cl and len(pattern_kq_cl) >= kq_length:
            for i in range(0, len(pattern_kq_cl) - kq_length, kq_length):
                pattern_segment = tuple(pattern_kq_cl[i:i + kq_length])
                if pattern_segment == tuple(recent_kq):
                    next_result = pattern_kq_cl[i + kq_length] if i + kq_length < len(pattern_kq_cl) else None
                    if next_result:
                        pattern_key = (pattern_segment, pattern_row['id'])
                        if pattern_key not in matched_patterns:
                            total_matches += 1
                            if next_result == 'C':
                                total_c_count += 1
                            else:
                                total_l_count += 1
                            matched_patterns.add(pattern_key)

    if total_matches == 0:
        for pattern_row in db_patterns:
            pattern = pattern_row['pattern'].split()
            pattern_kq_list, pattern_kq_cl, _ = standardize_kq("".join(pattern))
            if pattern_kq_cl:
                total_c_count += pattern_kq_cl.count('C')
                total_l_count += pattern_kq_cl.count('L')
                total_matches += len(pattern_kq_cl)

    if total_matches == 0:
        return {'error': 'Không có mẫu phù hợp.'}

    c_percentage = (total_c_count / total_matches) * 100 if total_matches > 0 else 0
    l_percentage = (total_l_count / total_matches) * 100 if total_matches > 0 else 0
    prediction = 'C' if c_percentage > l_percentage else 'L' if l_percentage > c_percentage else 'C'

    print(f"Matches: {total_matches}, C: {total_c_count}, L: {total_l_count}")
    print(f"C%: {c_percentage}, L%: {l_percentage}, Pred: {prediction}")

    last_prediction = prediction
    number_stats = calculate_number_stats(kq_list, db_patterns)

    return {
        'prediction': prediction,
        'total_matches': total_matches,
        'c_percentage': round(c_percentage, 2),
        'l_percentage': round(l_percentage, 2),
        'number_stats': number_stats
    }

def simulate_game(kq_input, kq_length, db_patterns, method="default", initial_capital=0, min_bet=0, bet_amount=0, lose_streak_bet_increase=None, win_streak_bet_increase=None):
    kq_list, kq_cl, format_type = standardize_kq(kq_input)
    if not kq_cl:
        return {'error': format_type}
    
    if len(kq_cl) < kq_length:
        return {'error': f'KQ chưa đủ {kq_length} kết quả.'}

    sim_win_count = 0
    sim_lose_count = 0
    sim_win_streak = 0
    sim_lose_streak = 0
    sim_max_win_streak = 0
    sim_max_lose_streak = 0
    sim_results = []
    capital = initial_capital if initial_capital > 0 else 0

    lose_streak_conditions = {int(k): float(v) for k, v in (lose_streak_bet_increase or {}).items()}
    win_streak_conditions = {int(k): float(v) for k, v in (win_streak_bet_increase or {}).items()}

    for i in range(kq_length, len(kq_cl)):
        current_segment = kq_cl[i - kq_length:i]
        current_segment_input = " ".join(current_segment)
        result = analyze_kq(current_segment_input, kq_length, db_patterns, method)
        if 'error' in result:
            continue

        prediction = result['prediction']
        c_percentage = result['c_percentage']
        l_percentage = result['l_percentage']
        actual = kq_cl[i]
        prediction_with_percent = f"{prediction} {c_percentage if prediction == 'C' else l_percentage}%"

        bet = bet_amount if bet_amount > 0 else (min_bet if min_bet > 0 else 0)
        if sim_lose_streak in lose_streak_conditions:
            bet *= lose_streak_conditions[sim_lose_streak]
        elif sim_win_streak in win_streak_conditions:
            bet *= win_streak_conditions[sim_win_streak]

        if capital < bet:
            bet = max(0, capital)

        profit_loss = bet * 0.96 if prediction == actual else -bet
        capital += profit_loss

        if prediction == actual:
            sim_win_count += 1
            sim_win_streak += 1
            sim_lose_streak = 0
            sim_max_win_streak = max(sim_max_win_streak, sim_win_streak)
        else:
            sim_lose_count += 1
            sim_lose_streak += 1
            sim_win_streak = 0
            sim_max_lose_streak = max(sim_max_lose_streak, sim_lose_streak)

        sim_results.append({
            'prediction': prediction_with_percent,
            'actual': actual,
            'used_kq': current_segment_input,
            'bet_amount': round(bet, 2),
            'profit_loss': round(profit_loss, 2),
            'capital': round(capital, 2)
        })

        if capital < 0:
            break

    return {
        'win_count': sim_win_count,
        'lose_count': sim_lose_count,
        'max_win_streak': sim_max_win_streak,
        'max_lose_streak': sim_max_lose_streak,
        'results': sim_results,
        'initial_kq': kq_input,
        'initial_capital': initial_capital,
        'min_bet': min_bet,
        'final_capital': round(capital, 2),
        'profit_loss': round(capital - initial_capital, 2)
    }

def ai_predict(kq_input, kq_length, db_patterns):
    kq_list, kq_cl, format_type = standardize_kq(kq_input)
    if not kq_cl:
        return {'error': format_type}

    if len(kq_cl) < kq_length:
        return {'error': f'KQ chưa đủ {kq_length} kết quả.'}

    return {'error': 'AI đang phát triển.'}

@app.route('/', methods=['GET', 'POST'])
def index():
    global current_kq, last_prediction, win_count, lose_count, win_streak, lose_streak, max_win_streak, max_lose_streak

    init_db()

    db = get_db()
    c = db.cursor()
    c.execute("SELECT * FROM kq_patterns")
    db_patterns = c.fetchall()

    c.execute("SELECT * FROM history ORDER BY timestamp DESC LIMIT 1")
    history_row = c.fetchone()
    highest_win_streak = history_row['highest_win_streak'] if history_row else 0
    highest_lose_streak = history_row['highest_lose_streak'] if history_row else 0

    if 'state' not in session:
        session['state'] = 'phan_tich'
    if 'tab' not in session:
        session['tab'] = 'analyze'

    result = None
    sim_result = None
    ai_result = None
    selected_kq_length = 4
    update_kq_length = 4
    sim_kq_length = 4
    sim_method = "default"
    initial_capital = 0
    min_bet = 0
    bet_amount = 0
    real_kq_input = ""

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
            session['state'] = 'phan_tich'
            session['tab'] = 'analyze'
            return render_template('index.html', current_kq=current_kq, selected_kq_length=selected_kq_length, update_kq_length=update_kq_length, sim_kq_length=sim_kq_length, sim_method=sim_method, initial_capital=initial_capital, min_bet=min_bet, bet_amount=bet_amount, real_kq_input=real_kq_input, win_count=win_count, lose_count=lose_count, win_streak=win_streak, lose_streak=lose_streak, max_win_streak=max_win_streak, max_lose_streak=max_lose_streak, highest_win_streak=highest_win_streak, highest_lose_streak=highest_lose_streak, state=session['state'], tab=session['tab'], result=result, sim_result=sim_result, ai_result=ai_result)

        if 'tab' in request.form:
            session['tab'] = request.form['tab']

        if 'kq_input' in request.form:
            kq_input = request.form.get('kq_input', '')
            selected_kq_length = int(request.form.get('kq_length', 4))
            if kq_input:
                kq_list, kq_cl, format_type = standardize_kq(kq_input)
                if kq_cl:
                    current_kq = " ".join(kq_cl)
                    result = analyze_kq(kq_input, selected_kq_length, db_patterns)
                    if not result.get('error'):
                        session['state'] = 'cap_nhat'
                        c.execute("INSERT INTO kq_patterns (pattern, format, timestamp) VALUES (?, ?, ?)",
                                  (kq_input, format_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        db.commit()

        if 'real_kq_input' in request.form:
            real_kq_input = request.form.get('real_kq_input', '')
            update_kq_length = int(request.form.get('update_kq_length', 4))
            if real_kq_input:
                real_kq_list, real_kq_cl, format_type = standardize_kq(real_kq_input)
                if real_kq_cl:
                    current_kq_list = current_kq.split() if current_kq else []
                    current_kq_list.extend(real_kq_cl)
                    current_kq = " ".join(current_kq_list)

                    c.execute("INSERT INTO kq_patterns (pattern, format, timestamp) VALUES (?, ?, ?)",
                              (real_kq_input, format_type, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    db.commit()

                    if last_prediction and real_kq_cl:
                        actual_result = real_kq_cl[-1]
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

                        if max_win_streak > highest_win_streak:
                            highest_win_streak = max_win_streak
                        if max_lose_streak > highest_lose_streak:
                            highest_lose_streak = max_lose_streak
                        c.execute("INSERT INTO history (highest_win_streak, highest_lose_streak, timestamp) VALUES (?, ?, ?)",
                                  (highest_win_streak, highest_lose_streak, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        db.commit()

                    result = analyze_kq(current_kq, update_kq_length, db_patterns)

        if 'sim_kq_input' in request.form:
            sim_kq_input = request.form.get('sim_kq_input', '')
            sim_kq_length = int(request.form.get('sim_kq_length', 4))
            sim_method = request.form.get('sim_method', 'default')
            initial_capital = float(request.form.get('initial_capital', 0))
            min_bet = float(request.form.get('min_bet', 0))
            bet_amount = float(request.form.get('bet_amount', 0))

            lose_streak_bet_increase = {}
            for streak in range(1, 6):
                multiplier = request.form.get(f'lose_streak_{streak}', '')
                if multiplier:
                    lose_streak_bet_increase[streak] = float(multiplier)

            win_streak_bet_increase = {}
            for streak in range(1, 6):
                multiplier = request.form.get(f'win_streak_{streak}', '')
                if multiplier:
                    win_streak_bet_increase[streak] = float(multiplier)

            if sim_kq_input:
                sim_result = simulate_game(sim_kq_input, sim_kq_length, db_patterns, sim_method, initial_capital, min_bet, bet_amount, lose_streak_bet_increase, win_streak_bet_increase)
                if not sim_result.get('error'):
                    c.execute("INSERT INTO simulations (pattern, result, timestamp) VALUES (?, ?, ?)",
                              (sim_kq_input, json.dumps(sim_result), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    db.commit()

        if 'ai_predict' in request.form:
            ai_kq_input = request.form.get('ai_kq_input', '')
            ai_kq_length = int(request.form.get('ai_kq_length', 4))
            if ai_kq_input:
                ai_result = ai_predict(ai_kq_input, ai_kq_length, db_patterns)

    db.close()
    return render_template('index.html', current_kq=current_kq, selected_kq_length=selected_kq_length, update_kq_length=update_kq_length, sim_kq_length=sim_kq_length, sim_method=sim_method, initial_capital=initial_capital, min_bet=min_bet, bet_amount=bet_amount, real_kq_input=real_kq_input, win_count=win_count, lose_count=lose_count, win_streak=win_streak, lose_streak=lose_streak, max_win_streak=max_win_streak, max_lose_streak=max_lose_streak, highest_win_streak=highest_win_streak, highest_lose_streak=highest_lose_streak, state=session['state'], tab=session['tab'], result=result, sim_result=sim_result, ai_result=ai_result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)