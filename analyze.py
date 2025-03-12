def analyze_data(kq_input, kq_length):
    # Giả định logic phân tích dữ liệu
    if not kq_input or len(kq_input) < kq_length:
        return {"error": "Dữ liệu không đủ!"}
    
    current_kq = kq_input[-kq_length:]
    # Đếm số lần xuất hiện C/L và các số 0-4
    c_count = current_kq.count('C')
    l_count = current_kq.count('L')
    total = len(current_kq)
    c_percentage = (c_count / total * 100) if total > 0 else 0
    l_percentage = (l_count / total * 100) if total > 0 else 0
    
    number_stats = {str(i): (current_kq.count(str(i)) / total * 100) for i in range(5)}
    prediction = 'C' if c_percentage > l_percentage else 'L'
    
    return {
        "current_kq": current_kq,
        "total_matches": total,
        "c_percentage": round(c_percentage, 2),
        "l_percentage": round(l_percentage, 2),
        "number_stats": {k: round(v, 2) for k, v in number_stats.items()},
        "prediction": prediction
    }