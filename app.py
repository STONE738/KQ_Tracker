 
from flask import Flask, render_template, request

app = Flask(__name__)

# Dữ liệu mẫu ban đầu (30 chuỗi giả lập)
data_samples = [
    "C C C C C L C L C C C C C L C C C L C C L C C L L C C C C C L C C L L C C L C L C L C L L L",
    "L L L L L C L L L C C C C C L C C L L L C C L L L C C L L L C L C L L L C L C C L L L L L C C C C C C L",
    "C L C C C L C L L C C C L C C C L C C C L C C L C C L L L L C C C L L L C L L C L L C L C C L L L L L L L L",
    "C C L C L L C L L L C C C L C C L L C C C L C C C C L C L C C C C L L L C C L C L C C C L C L L L C L C C L",
    "L C L C L L L L L C L C L C L C L L L L C L C L L L L C C L C L L C L L L L L C C L L C L L C L L L L",
    "C C C L L L L L L L L C C C L C C C L C L L C C C C L C L C L L L C C C C C C C C L C C C C L C L L L",
    "C L L L L C L L L C C L L C C L L L C C L L L C C L C L L L C L L L L C C C C L L L L C C L L C C L L",
    "L L L C L C C L C C L C L C C L L L L C L L L L L L L L C C C L C L L C L L L C L C L L C L L L C L C L",
    "L C C L C L C C L C L L C L C L C C L C L L C L L L C L L C C L C L C C L C C C C L L C L L C L C L C L",
    "L C L C L L L C C L L C C L L C C L C C L L L L C L L L L C L L L L C C C L C C C C C C L C L C C C L",
    "C C L L L L L L L C C C L C C C L C L L C C C C L C L C L L L C C C C C C C C L C C C C L C",
    "C L L L L C L L L L C C L L C C L L L C C L L L C C L C L L L C L L L L C C C C L L L L C C L L",
    "C C L C L C C L C C L L L C C C C L C L C L L C L L C L L L C L L C C C C L L L C L L L L L C L",
    "C L C C C L C L L L L C C C C C L L C L C C L C L C C L L C C L L L C C C L C C C C C L L C L C L",
    "L C L C L L L C C L L C C L L C C L C C L L L L C L L L L C L L L L C C C L L C C C C C C L C L",
    "L C C C L C C C L C C L C L C C C C C L L C L L L C C C C C C L C C C L L L L L C L L C L L L C",
    "L L L C C L L C L L C L L C L C L L L C C L C L C C C L C C C L C C L C L L C C C L C L C C C C",
    "L C C C L L C L L C L L C C L L L L L C C L C C L C C L L C C C L C C C C C L C L C C C C L C C",
    "L C C L L C L L C C L C C L L C L L L C C C L C L L C C C L L C L C C L L C L C",
    "C L L C C L C C L L C L L C C C L C L L C C L C L C C L L C C L C L L C L C C L",
    "C C L C L L C C L C L C C L L L C L C C L C L L C C C L L C L C C L L C L L C C",
    "L L C C L C L C C L L C C L C L C L L C C L C C L L C L C C L L C C L C L C L C",
    "C L C L C C L L C C C L C L L C L C C L L C C L C L C L C C L L C L C C L C L L",
    "L C L C C L C L L C C C L C L C L C C L L C L C C L C L L C C L C L C C L L C C",
    "C C L L C L C C L C L L C C C L C L C L L C C L C C L L C C L C L C L C C L L C",
    "L L C L C C L C L C C L L C C C L C L L C C L C L C L C C L L C C L C L C L C L",
    "C L C C L L C C L C L C L C C L L C C L C L C L C C L L C C L C L C C L L C L C",
    "L C L C C L L C C L C L C C L L C C L C L C L L C C C L C L C L C C L L C L C C",
    "C C L C L C L C C L L C C L C L C L L C C L C C L C L C L C C L L C C L C L C L",
    "L L C C L C L C C L C L L C C C L C L C L C C L L C C L C L C L C C L L C C L C"]

# Danh sách lưu KQ thực tế từ người dùng
real_kq = []

@app.route("/", methods=["GET", "POST"])
def index():
    global real_kq
    result = None
    if request.method == "POST":
        kq_input = request.form["kq_input"].strip().upper()
        kq_list = kq_input.split()
        if all(x in ["C", "L"] for x in kq_list):
            real_kq.extend(kq_list)
            if len(real_kq) > 50:
                real_kq = real_kq[-50:]
            result = process_kq(kq_input)
        else:
            result = "Dữ liệu không hợp lệ! Chỉ nhập C hoặc L, cách nhau bằng khoảng trắng."
    
    current_kq = " ".join(real_kq[-5:] if len(real_kq) >= 5 else real_kq)
    return render_template("index.html", result=result, current_kq=current_kq)

def process_kq(kq_input):
    matches = []
    kq_input_str = kq_input
    for sample in data_samples:
        if kq_input_str in sample:
            matches.append(sample)
    
    if matches:
        c_count = sum(1 for match in matches for i in range(len(match.split())) 
                      if kq_input_str in " ".join(match.split()[:i+1]) and i + 1 < len(match.split()) and match.split()[i+1] == "C")
        l_count = sum(1 for match in matches for i in range(len(match.split())) 
                      if kq_input_str in " ".join(match.split()[:i+1]) and i + 1 < len(match.split()) and match.split()[i+1] == "L")
        total = c_count + l_count
        c_percentage = (c_count / total) * 100 if total > 0 else 0
        l_percentage = (l_count / total) * 100 if total > 0 else 0
        return {
            "total_matches": len(matches),
            "c_percentage": round(c_percentage, 2),
            "l_percentage": round(l_percentage, 2)
        }
    else:
        return {"total_matches": 0, "c_percentage": 0, "l_percentage": 0}

if __name__ == "__main__":
    app.run(debug=True)