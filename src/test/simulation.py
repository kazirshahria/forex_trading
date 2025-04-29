"""Simulate a funded account winning and losing trades in the Forex market and print the APPT"""

import random
import numpy as np

# Account information
WINS = 0
LOSSES = 0
WINS_ARRAY = []
LOSSES_ARRAY = []
STARTING_BALANCE = 500
BALANCE = 500

# Risk management
MIN_RISK = 0.01
MAX_RISK = 0.10

# Profit and risk percentage
MIN_PROFIT_PERCT = 0.01
MAX_PROFIT_PERCT = 0.10
MIN_RISK_PERCT = MIN_PROFIT_PERCT * 2
MAX_RISK_PERCT = MAX_PROFIT_PERCT * 2

# Goal
BALANCE_GOAL = 100000

# Winning probability
THRESHOLD = 0.30

while BALANCE < BALANCE_GOAL:

    trade_prob = random.uniform(0, 1)
    risk_perct = random.uniform(MIN_RISK, MAX_RISK)
    risk_balance = BALANCE * risk_perct

    # Winning trade
    if THRESHOLD < trade_prob:
        
        WINS += 1

        # Random profit percent between 1-10%
        profit_perct = random.uniform(MIN_PROFIT_PERCT, MAX_PROFIT_PERCT)

        win_value = risk_balance * profit_perct
        BALANCE += win_value
        WINS_ARRAY.append(win_value)

    # Losing trade
    else:

        LOSSES += 1

        # Random loss percent between 2-20%
        loss_perct = random.uniform(MIN_RISK_PERCT, MAX_RISK_PERCT)
        
        loss_value = risk_balance * loss_perct
        BALANCE -= risk_balance * loss_perct
        LOSSES_ARRAY.append(loss_value)

    # Go broke
    if BALANCE <= STARTING_BALANCE * 0.50:
        print(f"Lost 50% of account balance with a {(1-THRESHOLD)*100}% win rate!")
        break

    print(f"Wins: {WINS} | Losses: {LOSSES}")

TOTAL_TRADES = WINS + LOSSES
WINS_RATE = WINS / TOTAL_TRADES
WINS_MEAN = (np.array(WINS_ARRAY)).mean()
LOSSES_MEAN = (np.array(LOSSES_ARRAY)).mean()
APPT = (WINS_MEAN * WINS_RATE) + (LOSSES_MEAN * (1-WINS_RATE))

print(f"Balance: ${BALANCE.__round__(2)}")
print(f"Total Trades: {TOTAL_TRADES}")
print(f"Avg. Win: ${round(WINS_MEAN, 2)} | Avg. Loss: ${round(LOSSES_MEAN, 2)}")
print(f"APPT: {round(APPT, 2)}")
