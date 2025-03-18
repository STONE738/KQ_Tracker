import json
import os

# Đường dẫn đến file JSON lưu trữ tài khoản
USER_FILE = "users.json"

def load_users():
    """Tải danh sách người dùng từ file JSON"""
    if not os.path.exists(USER_FILE):
        return {}
    with open(USER_FILE, 'r') as f:
        return json.load(f)

def save_users(users):
    """Lưu danh sách người dùng vào file JSON"""
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

def register_user(username, password):
    """Đăng ký người dùng mới"""
    users = load_users()
    if username in users:
        return False, "Tên đăng nhập đã tồn tại!"
    users[username] = password
    save_users(users)
    return True, "Đăng ký thành công! Vui lòng đăng nhập."

def login_user(username, password):
    """Đăng nhập người dùng"""
    users = load_users()
    if username in users and users[username] == password:
        return True, "Đăng nhập thành công!"
    return False, "Sai tên đăng nhập hoặc mật khẩu!"