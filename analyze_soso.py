def analyze_soso_data(soso_input, soso_length=6):  # Mặc định 6 số
    # Chuyển chuỗi đầu vào thành danh sách số
    soso_list = [int(s) for s in soso_input.replace(' ', '') if s.isdigit() and int(s) in range(10)]

    if len(soso_list) < soso_length:
        return {'error': f'Chuỗi số phải có ít nhất {soso_length} số!'}

    # Tính tần suất xuất hiện của từng số (0-9)
    number_stats = {str(i): 0 for i in range(10)}
    for num in soso_list:
        number_stats[str(num)] += 1
    total_count = len(soso_list)
    for key in number_stats:
        number_stats[key] = round((number_stats[key] / total_count) * 100, 2) if total_count > 0 else 0

    # Dự đoán số tiếp theo (lấy số có tần suất cao nhất)
    prediction = max(number_stats.items(), key=lambda x: x[1])[0] if total_count > 0 else '?'
    prediction_rate = number_stats[prediction] if total_count > 0 else 0

    return {
        'total_count': total_count,
        'number_stats': number_stats,
        'prediction': prediction,
        'prediction_rate': prediction_rate
    }