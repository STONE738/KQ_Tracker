from flask import Flask, render_template, request

app = Flask(__name__)

# Dữ liệu mẫu ban đầu (30 chuỗi KQ)
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
    "L L C C L C L C C L C L L C C C L C L C L C C L L C C L C L C L C C L L C C L C"
]

# Danh sách lưu KQ thực tế cho mỗi phiên (reset khi New Game)
real_kq = []

@app.route("/", methods=["GET", "POST"])
def index():
    global real_kq
    result = None
    if request.method == "POST":
        # Xử lý nút New Game
        if "new_game" in request.form:
            real_kq = []  # Reset chuỗi KQ
            return render_template("index.html", result="Đã tạo mới game!", current_kq="")
        
        # Xử lý nhập KQ
        kq_input = request.form["kq_input"].strip().upper()
        # Chuyển định dạng liền nhau (CLCC) thành cách nhau (C L C C)
        kq_list = []
        if len(kq_input.replace(" ", "")) in [4, 5]:  # Chỉ chấp nhận 4 hoặc 5 KQ
            if " " in kq_input:
                kq_list = kq_input.split()  # Nếu đã cách nhau
            else:
                # Chuyển từ liền nhau (CLCC) thành danh sách
                for char in kq_input:
                    if char in ["C", "L"]:
                        kq_list.append(char)
            if len(kq_list) in [4, 5] and all(x in ["C", "L"] for x in kq_list):
                real_kq.extend(kq_list)
                if len(real_kq) > 50:
                    real_kq = real_kq[-50:]  # Giới hạn 50 KQ
                result = process_kq(" ".join(kq_list))  # Chuyển thành chuỗi để tra cứu
            else:
                result = "Dữ liệu không hợp lệ! Chỉ nhập 4 hoặc 5 KQ (C hoặc L)."
        else:
            result = "Dữ liệu không hợp lệ! Vui lòng nhập 4 hoặc 5 KQ."

    current_kq = " ".join(real_kq[-5:] if len(real_kq) >= 5 else real_kq)
    return render_template("index.html", result=result, current_kq=current_kq)

def process_kq(kq_input):
    matches = []
    for sample in data_samples:
        if kq_input in sample:
            matches.append(sample)
    
    if matches:
        c_count = sum(1 for match in matches for i in range(len(match.split())) 
                      if kq_input in " ".join(match.split()[:i+1]) and i + 1 < len(match.split()) and match.split()[i+1] == "C")
        l_count = sum(1 for match in matches for i in range(len(match.split())) 
                      if kq_input in " ".join(match.split()[:i+1]) and i + 1 < len(match.split()) and match.split()[i+1] == "L")
        total = c_count + l_count
        c_percentage = (c_count / total) * 100 if total > 0 else 0
        l_percentage = (l_count / total) * 100 if total > 0 else 0
        # Dự đoán KQ dựa trên tỷ lệ cao nhất
        prediction = "C" if c_percentage > l_percentage else "L" if l_percentage > c_percentage else "C/L"
        return {
            "total_matches": len(matches),
            "c_percentage": round(c_percentage, 2),
            "l_percentage": round(l_percentage, 2),
            "prediction": prediction
        }
    else:
        return {"total_matches": 0, "c_percentage": 0, "l_percentage": 0, "prediction": "Không dự đoán được"}

if __name__ == "__main__":
    app.run(debug=True)