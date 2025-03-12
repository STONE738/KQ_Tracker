import random

def simulate_data(sim_kq_input, sim_kq_length, initial_capital, min_bet, lose_streak_bet_increase, 
                  win_streak_bet_increase, use_custom_settings):
    if not sim_kq_input or len(sim_kq_input) < sim_kq_length:
        return {"error": "Dữ liệu không đủ!"}
    
    initial_kq = sim_kq_input[-sim_kq_length:]
    capital = initial_capital
    bet_amount = min_bet
    win_count = 0
    lose_count = 0
    max_win_streak = 0
    max_lose_streak = 0
    current_streak = 0
    streak_type = None
    results = []
    win_streak = 0
    lose_streak = 0

    # Đảm bảo lose_streak_bet_increase và win_streak_bet_increase là dict hợp lệ
    lose_streak_bet_increase = lose_streak_bet_increase or {}
    win_streak_bet_increase = win_streak_bet_increase or {}

    for i in range(len(initial_kq)):
        prediction = random.choice(['C', 'L', '0', '1', '2', '3', '4'])
        actual = initial_kq[i]
        if use_custom_settings:
            if streak_type == 'win' and win_streak in win_streak_bet_increase:
                bet_amount += win_streak_bet_increase.get(win_streak, 0)
            elif streak_type == 'lose' and lose_streak in lose_streak_bet_increase:
                bet_amount += lose_streak_bet_increase.get(lose_streak, 0)
        
        profit_loss = bet_amount if prediction == actual else -bet_amount
        capital += profit_loss
        results.append({
            'prediction': prediction,
            'actual': actual,
            'bet_amount': bet_amount,
            'profit_loss': profit_loss,
            'capital': capital
        })

        if prediction == actual:
            win_count += 1
            win_streak += 1
            lose_streak = 0
            if win_streak > max_win_streak:
                max_win_streak = win_streak
            streak_type = 'win'
        else:
            lose_count += 1
            lose_streak += 1
            win_streak = 0
            if lose_streak > max_lose_streak:
                max_lose_streak = lose_streak
            streak_type = 'lose'

    profit_loss = capital - initial_capital

    return {
        "initial_kq": initial_kq,
        "win_count": win_count,
        "lose_count": lose_count,
        "max_win_streak": max_win_streak,
        "max_lose_streak": max_lose_streak,
        "initial_capital": initial_capital,
        "final_capital": capital,
        "profit_loss": profit_loss,
        "results": results
    }