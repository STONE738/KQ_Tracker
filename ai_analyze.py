from Ai_Tracker.sample_data import get_sample_patterns

def convert_to_cl(kq):
    if kq in ['C', 'L']:
        return kq
    return 'C' if kq in ['0', '2', '4'] else 'L'

def find_cycle(kq_list):
    n = len(kq_list)
    for length in range(1, n // 2 + 1):
        for start in range(n - length):
            cycle = kq_list[start:start + length]
            is_cycle = True
            for i in range(start + length, n, length):
                if i + length > n:
                    break
                if kq_list[i:i + length] != cycle:
                    is_cycle = False
                    break
            if is_cycle and (n - start) >= 2 * length:
                return cycle
    return None

def ai_analyze_data(kq_input, kq_length=6):  # Mặc định 6 KQ
    kq_list = kq_input.upper().split()
    kq_list = [convert_to_cl(val) for val in kq_list]
    if len(kq_list) < kq_length:  # Chỉ yêu cầu đủ kq_length KQ để phân tích
        return {"error": f"Chuỗi KQ phải có ít nhất {kq_length} kết quả!"}

    # Tìm chu kỳ trong chuỗi KQ
    cycle = find_cycle(kq_list)
    prediction = ''
    prediction_rate = 0

    # Tính tỷ lệ thực tế
    total_c = kq_list.count('C')
    total_l = kq_list.count('L')
    total = len(kq_list)
    overall_c_percentage = round((total_c / total) * 100, 2) if total > 0 else 0
    overall_l_percentage = round((total_l / total) * 100, 2) if total > 0 else 0

    # Nếu tìm thấy chu kỳ
    if cycle:
        cycle_length = len(cycle)
        last_position = (len(kq_list) - 1) % cycle_length
        next_position = (last_position + 1) % cycle_length
        prediction = cycle[next_position]
        prediction_rate = 80.0
    else:
        prediction = 'C' if overall_c_percentage > overall_l_percentage else 'L'
        prediction_rate = overall_c_percentage if overall_c_percentage > overall_l_percentage else overall_l_percentage

    # Tính số lần khớp (dựa trên mẫu cũ để giữ giao diện đồng bộ)
    last_pattern = ' '.join(kq_list[-kq_length:])
    sample_patterns = get_sample_patterns()
    number_counts = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0}
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
                    total_matches += 1
                    matched_patterns.add(pattern)
                    break

    number_stats = {}
    for num in number_counts:
        number_stats[num] = round((number_counts[num] / total_matches) * 100, 1) if total_matches > 0 else 0

    return {
        "current_kq": ' '.join(kq_list),
        "total_matches": total_matches,
        "c_percentage": overall_c_percentage,
        "l_percentage": overall_l_percentage,
        "number_stats": number_stats,
        "prediction": prediction,
        "prediction_rate": prediction_rate
    }