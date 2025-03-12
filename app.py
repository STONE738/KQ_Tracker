from flask import Flask, request, render_template, redirect, url_for, session, flash
from datetime import datetime, timedelta
import sqlite3
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Kết nối database SQLite
def get_db():
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row
    return conn

# Đọc file JSON người dùng
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Lưu file JSON người dùng
def save_users(users):
    with open('users.json', 'w', encoding='utf-8') as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# Đọc file JSON admin
def load_admin():
    if os.path.exists('admin.json'):
        with open('admin.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"username": "admin", "password": "admin123", "role": "admin"}

# Lưu file JSON admin
def save_admin(admin):
    with open('admin.json', 'w', encoding='utf-8') as f:
        json.dump(admin, f, ensure_ascii=False, indent=4)

# Khởi tạo database và file JSON
def init_db():
    if not os.path.exists('users.db'):
        with get_db() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    user_id INTEGER,
                    background TEXT,
                    font_size TEXT,
                    circle_position TEXT,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            ''')
            # Khởi tạo cài đặt mặc định cho admin (user_id = 0)
            conn.execute('INSERT OR IGNORE INTO settings (user_id, background, font_size, circle_position) VALUES (?, ?, ?, ?)',
                         (0, 'gradient', 'medium', 'middle'))
            conn.commit()
    if not os.path.exists('users.json'):
        save_users({})
    if not os.path.exists('admin.json'):
        save_admin({"username": "admin", "password": "admin123", "role": "admin"})

init_db()

from analyze import analyze_data
from simulate import simulate_data

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'user_id' not in session or 'username' not in session:
        return redirect(url_for('login'))
    
    tab = request.form.get('tab', 'analyze')
    users = load_users()
    admin = load_admin()
    # Tìm user hiện tại, nếu không tìm thấy thì dùng admin hoặc None
    current_user = next((u for u in users.values() if u['id'] == session['user_id']), admin if session['username'] == admin['username'] else None)
    if not current_user:
        flash('Không tìm thấy thông tin người dùng!')
        return redirect(url_for('login'))
    
    current_kq = session.get('current_kq', '')
    selected_kq_length = session.get('selected_kq_length', 4)
    use_custom_settings = session.get('use_custom_settings', False)
    initial_capital = session.get('initial_capital', 100000)
    min_bet = session.get('min_bet', 1000)
    lose_streak_bet_increase = session.get('lose_streak_bet_increase', {})
    win_streak_bet_increase = session.get('win_streak_bet_increase', {})

    if request.method == 'POST':
        if 'kq_input' in request.form:
            kq_input = request.form['kq_input']
            kq_length = int(request.form['kq_length'])
            result = analyze_data(kq_input, kq_length)
            if result:
                session['current_kq'] = result['current_kq']
                session['selected_kq_length'] = kq_length
            return render_template('index.html', tab=tab, result=result, current_kq=session['current_kq'],
                                  selected_kq_length=session['selected_kq_length'], username=session['username'],
                                  role=current_user['role'], settings=None)
        elif 'sim_kq_input' in request.form:
            sim_kq_input = request.form['sim_kq_input']
            sim_kq_length = int(request.form['sim_kq_length'])
            sim_result = simulate_data(sim_kq_input, sim_kq_length, initial_capital, min_bet,
                                      lose_streak_bet_increase, win_streak_bet_increase, use_custom_settings)
            if sim_result:
                session['sim_kq_length'] = sim_kq_length
            return render_template('index.html', tab=tab, sim_result=sim_result, current_kq=session.get('current_kq'),
                                  selected_kq_length=session.get('selected_kq_length'), use_custom_settings=use_custom_settings,
                                  initial_capital=initial_capital, min_bet=min_bet, lose_streak_bet_increase=lose_streak_bet_increase,
                                  win_streak_bet_increase=win_streak_bet_increase, username=session['username'],
                                  role=current_user['role'], settings=None)

    with get_db() as conn:
        settings = conn.execute('SELECT * FROM settings WHERE user_id = ?', (session['user_id'],)).fetchone()
    return render_template('index.html', tab=tab, current_kq=current_kq, selected_kq_length=selected_kq_length,
                          use_custom_settings=use_custom_settings, initial_capital=initial_capital, min_bet=min_bet,
                          lose_streak_bet_increase=lose_streak_bet_increase, win_streak_bet_increase=win_streak_bet_increase,
                          username=session['username'], role=current_user['role'], settings=dict(settings) if settings else {})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        admin = load_admin()
        user = next((u for u in users.values() if u['username'] == username and u['password'] == password), None)
        if not user and admin['username'] == username and admin['password'] == password:
            user = admin
        if user:
            session['user_id'] = user.get('id', 0)  # ID 0 cho admin
            session['username'] = user['username']
            session['role'] = user['role']
            return redirect(url_for('index'))
        else:
            flash('Sai tên đăng nhập hoặc mật khẩu!')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = load_users()
        if username in [u['username'] for u in users.values()]:
            flash('Tên đăng nhập đã tồn tại!')
        else:
            new_id = max((u['id'] for u in users.values()), default=0) + 1
            users[new_id] = {"id": new_id, "username": username, "password": password, "role": "user", "points": 0, "usage_time": 0}
            save_users(users)
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/save_settings', methods=['POST'])
def save_settings():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
    
    background = request.form.get('background')
    font_size = request.form.get('font_size')
    circle_position = request.form.get('circle_position')
    
    with get_db() as conn:
        conn.execute('INSERT OR REPLACE INTO settings (user_id, background, font_size, circle_position) VALUES (?, ?, ?, ?)', 
                     (session['user_id'], background, font_size, circle_position))
        conn.commit()
    flash('Cài đặt đã được lưu!')
    return redirect(url_for('index'))

@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
    
    users = load_users()
    if request.method == 'POST':
        user_id = request.form['user_id']
        points = request.form.get('points')
        usage_time = request.form.get('usage_time')
        if str(user_id) in users:
            if points:
                users[str(user_id)]['points'] = int(points)
            if usage_time:
                users[str(user_id)]['usage_time'] = int(usage_time)
            save_users(users)
        flash('Cập nhật thành công!')
    
    return render_template('manage_users.html', users=users)

@app.route('/update_data', methods=['GET', 'POST'])
def update_data():
    if 'user_id' not in session or session['role'] != 'admin':
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        new_data = request.form.get('new_data')
        with open('data.txt', 'a', encoding='utf-8') as f:
            f.write(new_data + '\n')
        flash('Dữ liệu đã được cập nhật!')
    return render_template('update_data.html')

if __name__ == '__main__':
    app.run(debug=True)