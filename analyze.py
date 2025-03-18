from Ai_Tracker.sample_data import get_sample_patterns

def convert_to_cl(kq):
    if kq in ['C', 'L']:
        return kq
    return 'C' if kq in ['0', '2', '4'] else 'L'

def analyze_data(kq_input, kq_length=6):  # Mặc định 6 KQ
    kq_list = kq_input.upper().split()
    kq_list = [convert_to_cl(val) for val in kq_list]
    if len(kq_list) < kq_length:  # Chỉ yêu cầu đủ kq_length KQ để phân tích
        return {"error": f"Chuỗi KQ phải có ít nhất {kq_length} kết quả!"}

    last_pattern = ' '.join(kq_list[-kq_length:])

    # Đếm số lần khớp với mẫu
    sample_patterns = get_sample_patterns()
    c_count = 0
    l_count = 0
    total_matches = 0
    matched_patterns = set()

    for pattern, pattern_type, _ in sample_patterns:
        if pattern_type == "letter":
            pattern_list = pattern.split()
            if len(pattern_list) <= kq_length:
                continue
            for i in range(len(pattern_list) - kq_length):
                sample_prefix = ' '.join(pattern_list[i:i + kq_length])
                if sample_prefix == last_pattern:
                    next_result = pattern_list[i + kq_length] if i + kq_length < len(pattern_list) else None
                    if next_result == 'C':
                        c_count += 1
                    elif next_result == 'L':
                        l_count += 1
                    total_matches += 1
                    matched_patterns.add(pattern)
                    break
        elif pattern_type == "number":
            decoded_pattern = ' '.join(char for char in pattern if char in ['0', '1', '2', '3', '4'])
            decoded_list = decoded_pattern.split()
            if len(decoded_list) <= kq_length:
                continue
            converted_list = [convert_to_cl(num) for num in decoded_list]
            for i in range(len(converted_list) - kq_length):
                sample_prefix = ' '.join(converted_list[i:i + kq_length])
                if sample_prefix == last_pattern:
                    next_result = converted_list[i + kq_length] if i + kq_length < len(converted_list) else None
                    if next_result == 'C':
                        c_count += 1
                    elif next_result == 'L':
                        l_count += 1
                    total_matches += 1
                    matched_patterns.add(pattern)
                    break

    # Tính tỷ lệ từ mẫu
    sample_c_percentage = round((c_count / total_matches) * 100, 2) if total_matches > 0 else 0
    sample_l_percentage = round((l_count / total_matches) * 100, 2) if total_matches > 0 else 0
    prediction = 'C' if sample_c_percentage > sample_l_percentage else 'L'
    prediction_rate = sample_c_percentage if sample_c_percentage > sample_l_percentage else sample_l_percentage

    return {
        "current_kq": ' '.join(kq_list),
        "total_matches": total_matches,
        "sample_c_percentage": sample_c_percentage,
        "sample_l_percentage": sample_l_percentage,
        "prediction": prediction,
        "prediction_rate": prediction_rate
    }