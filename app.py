from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
import os
from datetime import timedelta
from analyze import analyze_data
from ai_analyze import ai_analyze_data
from analyze_soso import analyze_soso_data
from simulate import simulate_game
from users import register_user, login_user, load_users

app = Flask(__name__, static_folder='static')
app.secret_key = 'your_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
Session(app)

# Kiểm tra đăng nhập chỉ cho các route cần
def login_required(f):
    def wrap(*args, **kwargs):
        if 'username' not in session:
            return jsonify({'error': 'Vui lòng đăng nhập để sử dụng chức năng này!'})
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__
    return wrap

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login_page', methods=['GET'])
def login_page():
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/check_login', methods=['GET'])
def check_login():
    if 'username' in session:
        return jsonify({'logged_in': True, 'username': session['username']})
    return jsonify({'logged_in': False})

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    success, message = login_user(username, password)
    if success:
        session['username'] = username
        session.permanent = True
        return jsonify({'success': True, 'username': username})
    return jsonify({'success': False, 'message': message})

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    return jsonify({'success': True})

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']
    
    success, message = register_user(username, password)
    return jsonify({'success': success, 'message': message})

@app.route('/forgot_password', methods=['POST'])
def forgot_password():
    username = request.form['username']
    users = load_users()
    if username not in users:
        return jsonify({'success': False, 'message': 'Tên đăng nhập không tồn tại!'})
    return jsonify({'success': True, 'message': 'Yêu cầu đã được gửi! Vui lòng kiểm tra email.'})

@app.route('/analyze', methods=['POST'])
@login_required
def analyze():
    kq_input = request.form.get('kq_input', '')
    kq_length = int(request.form.get('kq_length', 6))
    result = analyze_data(kq_input, kq_length)
    return jsonify(result)

@app.route('/ai_analyze', methods=['POST'])
@login_required
def ai_analyze():
    kq_input = request.form.get('kq_input', '')
    kq_length = int(request.form.get('kq_length', 6))
    result = ai_analyze_data(kq_input, kq_length)
    return jsonify(result)

@app.route('/analyze_soso', methods=['POST'])
def analyze_soso():
    soso_input = request.form.get('soso_input', '')
    soso_length = int(request.form.get('soso_length', 6))
    result = analyze_soso_data(soso_input, soso_length)
    return jsonify(result)

@app.route('/simulate', methods=['POST'])
@login_required
def simulate():
    kq_input = request.form.get('kq_input', '').strip()
    kq_length = int(request.form.get('kq_length', 6))
    prediction_tool = request.form.get('prediction_tool', 'analyze')
    initial_capital = float(request.form.get('initial_capital', 0))
    min_bet = float(request.form.get('min_bet', 0))
    use_betting = bool(request.form.get('use_betting', False))

    # Nhận dữ liệu JSON và chuyển thành dictionary
    win_streak_bet_increase_json = request.form.get('win_streak_bet_increase', '{}')
    lose_streak_bet_increase_json = request.form.get('lose_streak_bet_increase', '{}')
    import json
    win_streak_bet_increase = json.loads(win_streak_bet_increase_json)
    lose_streak_bet_increase = json.loads(lose_streak_bet_increase_json)

    # Kiểm tra và gán giá trị mặc định nếu thiếu
    win1 = float(win_streak_bet_increase.get('1', 0))
    win2 = float(win_streak_bet_increase.get('2', 0))
    win3 = float(win_streak_bet_increase.get('3', 0))
    win4 = float(win_streak_bet_increase.get('4', 0))
    win5 = float(win_streak_bet_increase.get('5', 0))
    lose1 = float(lose_streak_bet_increase.get('1', 0))
    lose2 = float(lose_streak_bet_increase.get('2', 0))
    lose3 = float(lose_streak_bet_increase.get('3', 0))
    lose4 = float(lose_streak_bet_increase.get('4', 0))
    lose5 = float(lose_streak_bet_increase.get('5', 0))

    # Debug dữ liệu nhận được
    print(f"Received - kq_input: {kq_input}, use_betting: {use_betting}, initial_capital: {initial_capital}, min_bet: {min_bet}, win1: {win1}, lose1: {lose1}")

    # Không cắt chuỗi KQ, gửi toàn bộ chuỗi thực tế
    kq_list = kq_input.split() if kq_input else []
    if len(kq_list) < kq_length + 1:
        return jsonify({'error': f'Chuỗi KQ phải có ít nhất {kq_length + 1} kết quả để mô phỏng!'})
    adjusted_kq_input = ' '.join(kq_list)

    result = simulate_game(
        adjusted_kq_input,
        kq_length,
        prediction_tool,
        initial_capital,
        min_bet,
        win1, win2, win3, win4, win5,
        lose1, lose2, lose3, lose4, lose5,
        use_betting
    )
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)