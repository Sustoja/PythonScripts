# Calculates the max. number of bitcoins to be issued
# First block reward was 50 BTC
# Reward is halved every 210.000 blocks (aprox. every 4 years)

current_reward = 50
reward_interval = 210000
total = 0

while current_reward > 0:
    total += current_reward * reward_interval
    current_reward /= 2

formatted_float = "{:,.2f}".format(total)
print("Max. BTC to ever be created: ", formatted_float)