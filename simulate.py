from analyze import analyze_data
from ai_analyze import ai_analyze_data

def simulate_game(kq_input, kq_length=6, prediction_tool="analyze", initial_capital=0, win_bets=None, lose_bets=None, use_betting=False):
    print("File simulate.py updated - version 22.0")

    # Khởi tạo giá trị mặc định cho win_bets và lose_bets nếu không có
    if not win_bets or not lose_bets:
        win_bets = [0] * 6
        lose_bets = [0] * 6

    print(f"use_betting: {use_betting}, initial_capital: {initial_capital}, win_bets: {win_bets}, lose_bets: {lose_bets}")
    
    # Kiểm tra dữ liệu đầu vào
    if not kq_input or kq_length < 6 or kq_length > 8:
        return {'error': 'Dữ liệu không hợp lệ'}

    kq_list = kq_input.upper().split()
    if len(kq_list) < kq_length + 1:
        return {'error': f'Chuỗi KQ phải có ít nhất {kq_length + 1} kết quả để mô phỏng!'}

    # Khởi tạo các biến
    capital = float(initial_capital) if use_betting else 0
    win_count = 0
    lose_count = 0
    total_rounds = 0
    max_win_streak = 0
    max_lose_streak = 0
    current_win_streak = 0
    current_lose_streak = 0
    max_profit = 0
    max_loss = 0
    round_details = []

    # Duyệt qua từng ván
    for i in range(kq_length, len(kq_list)):
        current_kq = ' '.join(kq_list[i - kq_length:i])
        actual = kq_list[i]

        # Dự đoán kết quả
        if prediction_tool == "analyze":
            result = analyze_data(current_kq, kq_length)
        else:
            result = ai_analyze_data(current_kq, kq_length)
        
        if "error" in result:
            return {'error': result['error']}
        prediction = result['prediction']
        prediction_rate = result.get('prediction_rate', 0)

        total_rounds += 1
        is_win = prediction == actual
        round_result = {
            'round': total_rounds,
            'prediction': prediction,
            'prediction_rate': round(prediction_rate, 2),
            'actual': actual
        }

        print(f"Ván {total_rounds}: Dự đoán = {prediction}, Thực tế = {actual}, Kết quả = {'Win' if is_win else 'Lose'}")

        # Đếm win_count và lose_count dựa trên KQ, không phụ thuộc vào cược
        if is_win:
            win_count += 1
            current_win_streak += 1
            current_lose_streak = 0
            max_win_streak = max(max_win_streak, current_win_streak)
        else:
            lose_count += 1
            current_lose_streak += 1
            current_win_streak = 0
            max_lose_streak = max(max_lose_streak, current_lose_streak)

        # Tính cược
        current_bet = 0
        if use_betting and initial_capital > 0:
            # Ván đầu tiên cược lose_bets[0]
            if total_rounds == 1:
                current_bet = lose_bets[0]
            else:
                # Dựa trên streak của ván trước để đặt cược
                if round_details[-1]['win_streak'] > 0:
                    current_bet = win_bets[min(round_details[-1]['win_streak'] - 1, 5)]
                else:
                    current_bet = lose_bets[min(round_details[-1]['lose_streak'] - 1, 5)]

            round_result['capital_before'] = capital
            round_result['bet'] = float(current_bet)

            profit_loss = 0
            if current_bet > 0:
                if capital < current_bet:
                    print(f"Capital too low: capital {capital} < current_bet {current_bet}")
                    round_result['capital_before'] = round(capital, 1)
                    round_result['bet'] = round(current_bet, 1)
                    round_result['capital_after'] = round(capital, 1)
                    round_result['profit_loss'] = 0
                    round_result['result'] = 'Win' if is_win else 'Lose'
                    round_result['win_streak'] = current_win_streak if is_win else 0
                    round_result['lose_streak'] = current_lose_streak if not is_win else 0
                    round_details.append(round_result)
                    continue

                capital -= current_bet

                if is_win:
                    profit_loss = current_bet * 0.95
                    capital += current_bet + profit_loss
                else:
                    profit_loss = -current_bet
                    capital += current_bet + profit_loss

                if profit_loss > 0:
                    max_profit = max(max_profit, profit_loss)
                elif profit_loss < 0:
                    max_loss = min(max_loss, profit_loss)

            else:
                profit_loss = 0  # Đảm bảo profit_loss = 0 khi current_bet = 0

            round_result['capital_before'] = round(round_result['capital_before'], 1)
            round_result['bet'] = round(round_result['bet'], 1)
            round_result['capital_after'] = round(capital, 1)
            round_result['profit_loss'] = round(profit_loss, 1)
            round_result['result'] = 'Win' if is_win else 'Lose'
            round_result['win_streak'] = current_win_streak if is_win else 0
            round_result['lose_streak'] = current_lose_streak if not is_win else 0
        else:
            round_result['bet'] = 0
            round_result['capital_before'] = round(capital, 1)
            round_result['capital_after'] = round(capital, 1)
            round_result['profit_loss'] = 0
            round_result['result'] = 'Win' if is_win else 'Lose'
            round_result['win_streak'] = current_win_streak if is_win else 0
            round_result['lose_streak'] = current_lose_streak if not is_win else 0

        round_details.append(round_result)

    final_capital = round(capital, 1)
    profit_loss = round(final_capital - initial_capital, 1) if use_betting else 0

    print(f"Returning - total_rounds: {total_rounds}, win_count: {win_count}, lose_count: {lose_count}, initial_capital: {initial_capital}, final_capital: {final_capital}, profit_loss: {profit_loss}, max_profit: {max_profit}, max_loss: {max_loss}")
    return {
        'total_rounds': total_rounds,
        'win_count': win_count,
        'lose_count': lose_count,
        'initial_capital': round(initial_capital, 1) if use_betting else 0,
        'final_capital': final_capital if use_betting else 0,
        'profit_loss': profit_loss,
        'max_profit': round(max_profit, 1) if use_betting else 0,
        'max_loss': round(max_loss, 1) if use_betting else 0,
        'max_win_streak': max_win_streak,
        'max_lose_streak': max_lose_streak,
        'round_details': round_details
    }