from analyze import analyze_data
from ai_analyze import ai_analyze_data

def simulate_game(kq_input, kq_length=6, prediction_tool="analyze", initial_capital=0, min_bet=0,
                  win1=0, win2=0, win3=0, win4=0, win5=0,
                  lose1=0, lose2=0, lose3=0, lose4=0, lose5=0, use_betting=False):
    print(f"use_betting: {use_betting}, initial_capital: {initial_capital}, min_bet: {min_bet}, win1: {win1}, lose1: {lose1}")  # Debug
    if not kq_input or kq_length < 6 or kq_length > 8:
        return {'error': 'Dữ liệu không hợp lệ'}

    kq_list = kq_input.upper().split()
    if len(kq_list) < kq_length + 1:
        return {'error': f'Chuỗi KQ phải có ít nhất {kq_length + 1} kết quả để mô phỏng!'}

    capital = float(initial_capital) if use_betting else 0
    current_bet = float(min_bet) if use_betting and (any([win1, win2, win3, win4, win5]) or any([lose1, lose2, lose3, lose4, lose5])) else 0
    win_streak = 0
    lose_streak = 0
    win_count = 0
    lose_count = 0
    total_rounds = 0
    max_win_streak = 0
    max_lose_streak = 0
    round_details = []
    max_profit = 0
    max_loss = 0

    for i in range(kq_length, len(kq_list)):
        current_kq = ' '.join(kq_list[i - kq_length:i])
        actual = kq_list[i]

        if prediction_tool == "analyze":
            result = analyze_data(current_kq, kq_length)
        else:
            result = ai_analyze_data(current_kq, kq_length)
        
        if "error" in result:
            return {'error': result['error']}
        prediction = result['prediction']

        total_rounds += 1
        round_result = {'round': total_rounds, 'prediction': prediction, 'actual': actual}

        if use_betting and initial_capital > 0 and current_bet > 0:
            if capital < current_bet or current_bet <= 0:
                print(f"Stopping simulation: capital {capital} < current_bet {current_bet} or current_bet <= 0")  # Debug
                break

            round_result['capital_before'] = capital
            round_result['bet'] = current_bet
            capital -= current_bet

            is_win = prediction == actual
            profit_loss = 0
            if is_win:
                win_streak += 1
                lose_streak = 0
                win_count += 1
                profit_loss = current_bet  # Lãi = +current_bet
                capital += current_bet * 2  # Hoàn vốn cược + lãi
                # Tăng cược dựa trên chuỗi thắng
                win_multipliers = {1: win1, 2: win2, 3: win3, 4: win4, 5: win5}
                win_multiplier = win_multipliers.get(win_streak, win5) / 100 if win_streak in win_multipliers else 0
                current_bet = (min_bet * (1 + win_multiplier)) if win_multiplier > 0 else current_bet
                max_win_streak = max(max_win_streak, win_streak)
            else:
                lose_streak += 1
                win_streak = 0
                lose_count += 1
                profit_loss = -current_bet  # Lỗ = -current_bet
                # Tăng cược dựa trên chuỗi thua
                lose_multipliers = {1: lose1, 2: lose2, 3: lose3, 4: lose4, 5: lose5}
                lose_multiplier = lose_multipliers.get(lose_streak, lose5) / 100 if lose_streak in lose_multipliers else 0
                current_bet = (min_bet * (1 + lose_multiplier)) if lose_multiplier > 0 else current_bet
                max_lose_streak = max(max_lose_streak, lose_streak)

            round_result['capital_after'] = capital
            round_result['profit_loss'] = profit_loss
            round_result['result'] = 'Win' if is_win else 'Lose'

            if profit_loss > 0:
                max_profit = max(max_profit, profit_loss)
            elif profit_loss < 0:
                max_loss = min(max_loss, profit_loss)
        else:
            if prediction == actual:
                win_streak += 1
                lose_streak = 0
                win_count += 1
                max_win_streak = max(max_win_streak, win_streak)
            else:
                lose_streak += 1
                win_streak = 0
                lose_count += 1
                max_lose_streak = max(max_lose_streak, lose_streak)
            round_result['bet'] = 0
            round_result['capital_before'] = capital
            round_result['capital_after'] = capital
            round_result['profit_loss'] = 0
            round_result['result'] = 'Win' if prediction == actual else 'Lose'

        round_details.append(round_result)

    final_capital = capital
    profit_loss = final_capital - initial_capital if use_betting else 0

    print(f"Returning - total_rounds: {total_rounds}, initial_capital: {initial_capital}, final_capital: {final_capital}, profit_loss: {profit_loss}, max_profit: {max_profit}, max_loss: {max_loss}, max_win_streak: {max_win_streak}, max_lose_streak: {max_lose_streak}")  # Debug
    return {
        'total_rounds': total_rounds,
        'win_count': win_count,
        'lose_count': lose_count,
        'initial_capital': initial_capital if use_betting else 0,
        'final_capital': final_capital if use_betting else 0,
        'profit_loss': profit_loss,
        'max_profit': max_profit if use_betting else 0,
        'max_loss': max_loss if use_betting else 0,
        'max_win_streak': max_win_streak,
        'max_lose_streak': max_lose_streak,
        'round_details': round_details
    }