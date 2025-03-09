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

# Danh sách lưu KQ thực tế và KQ đầu tiên tra cứu
real_kq = []  # Lưu KQ thực tế từ "Cập nhật"
initial_kq = ""  # Lưu KQ từ "Phân Tích"
selected_kq_length = 5  # Biến toàn cục cho "Phân Tích"
update_kq_length = 5  # Biến toàn cục cho "Cập nhật"

@app.route("/", methods=["GET", "POST"])
def index():
    global real_kq, initial_kq, selected_kq_length, update_kq_length
    result = None

    if request.method == "POST":
        # Lấy giá trị độ dài KQ từ select và lưu vào biến tương ứng
        selected_kq_length = int(request.form.get("kq_length", selected_kq_length))
        update_kq_length = int(request.form.get("update_kq_length", update_kq_length))

        # Xử lý nút New Game
        if "new_game" in request.form:
            real_kq = []
            initial_kq = ""
            selected_kq_length = 5
            update_kq_length = 5
            return render_template("index.html", result="Đã reset game!", current_kq="", real_kq_input="", selected_kq_length=selected_kq_length, update_kq_length=update_kq_length)

        # Xử lý nút Phân Tích
        if "kq_input" in request.form and request.form["kq_input"]:
            kq_input = request.form["kq_input"].strip().upper()
            kq_list = []
            if kq_input and all(x in ["C", "L"] for x in kq_input.replace(" ", "")):
                kq_list = kq_input.split() if " " in kq_input else list(kq_input)
                recent_kq = " ".join(kq_list[-selected_kq_length:]) if len(kq_list) >= selected_kq_length else " ".join(kq_list)
                initial_kq = recent_kq
                result = process_kq(initial_kq)
            else:
                result = "Dữ liệu không hợp lệ! Vui lòng nhập KQ (C hoặc L)."
            return render_template("index.html", result=result, current_kq=format_kq_display(initial_kq, real_kq), real_kq_input="", selected_kq_length=selected_kq_length, update_kq_length=update_kq_length)

        # Xử lý nút Cập nhật (Cập nhật và Phân Tích ngay lập tức với update_kq_length)
        if "real_kq_input" in request.form and request.form["real_kq_input"]:
            real_kq_input = request.form["real_kq_input"].strip().upper()
            if real_kq_input and all(x in ["C", "L"] for x in real_kq_input.replace(" ", "")):
                is_valid = True
                kq_list = real_kq_input.split() if " " in real_kq_input else list(real_kq_input)
                for i in range(len(kq_list) - 5):
                    if all(kq_list[i] == kq_list[i+j] for j in range(6)):
                        is_valid = False
                        break
                if is_valid:
                    real_kq.extend(kq_list)
                    if len(real_kq) > 50:
                        real_kq = real_kq[-50:]
                    # Tra cứu lại với update_kq_length KQ mới nhất từ real_kq
                    recent_kq = " ".join(real_kq[-update_kq_length:] if len(real_kq) >= update_kq_length else real_kq)
                    result = process_kq(recent_kq)
                else:
                    result = "Không hợp lệ! Không được nhập hơn 5 KQ giống nhau liên tiếp."
            else:
                result = "KQ thực tế không hợp lệ! Vui lòng nhập ít nhất 1 KQ (C hoặc L)."
            return render_template("index.html", result=result, current_kq=format_kq_display(initial_kq, real_kq), real_kq_input="", selected_kq_length=selected_kq_length, update_kq_length=update_kq_length)

    # Hiển thị mặc định
    current_kq = format_kq_display(initial_kq, real_kq)
    return render_template("index.html", result=result, current_kq=current_kq, real_kq_input="", selected_kq_length=selected_kq_length, update_kq_length=update_kq_length)

def format_kq_display(initial_kq, real_kq):
    # Ghép initial_kq với tối đa 50 KQ từ real_kq, xuống dòng mỗi 10 KQ
    all_kq = (initial_kq.split() if initial_kq else []) + real_kq
    if len(all_kq) > 50:
        all_kq = all_kq[-50:]
    if not all_kq:
        return ""
    result = []
    for i in range(0, len(all_kq), 10):
        chunk = " ".join(all_kq[i:i+10])
        result.append(chunk)
    return "<br>".join(result)

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
        if c_percentage > l_percentage:
            prediction = "C"
        elif l_percentage > c_percentage:
            prediction = "L"
        else:
            prediction = f"C/L ({c_percentage:.0f}%/{l_percentage:.0f}%)"
        return {
            "total_matches": len(matches),
            "c_percentage": round(c_percentage, 2),
            "l_percentage": round(l_percentage, 2),
            "prediction": prediction
        }
    else:
        return {"total_matches": 0, "c_percentage": 0, "l_percentage": 0, "prediction": "BỎ QUA"}

if __name__ == "__main__":
    app.run(debug=True)