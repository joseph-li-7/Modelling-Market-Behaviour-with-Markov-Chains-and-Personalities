# We are going to run a simulation of a pretend stock market with different kinds of people.
# Each person makes decisions based on their personality and how the market is doing.
# This program will track how their money grows or shrinks over 20 years.

import random  # This helps us make random decisions, like flipping coins.
import statistics  # This helps us calculate things like the average money people have.
import matplotlib.pyplot as plt  # This is for drawing graphs to see our results.

# Here are 4 types of people and how likely they are to stay in the market depending on how it's doing.
PERSONALITIES = {
    "risk_taker": {"stay_in_prob": {"up": 0.9, "down": 0.75, "flat": 0.8}},
    "cautious":   {"stay_in_prob": {"up": 0.95, "down": 0.4, "flat": 0.6}},
    "greedy":     {"stay_in_prob": {"up": 0.99, "down": 0.65, "flat": 0.7}},
    "average":    {"stay_in_prob": {"up": 0.85, "down": 0.5, "flat": 0.65}},
}

# This is a map of how the market moves: from "up", what are the chances it goes "down", "flat", "boom", or "crash".
BASE_MARKOV_TRANSITIONS = {
    "up": {"up": 0.4, "down": 0.3, "flat": 0.25, "crash": 0.025, "boom": 0.025},
    "down": {"up": 0.3, "down": 0.4, "flat": 0.25, "crash": 0.05, "boom": 0.0},
    "flat": {"up": 0.35, "down": 0.3, "flat": 0.3, "crash": 0.025, "boom": 0.025},
    "crash": {"up": 0.4, "down": 0.3, "flat": 0.25, "crash": 0.025, "boom": 0.025},
    "boom": {"up": 0.3, "down": 0.25, "flat": 0.4, "crash": 0.025, "boom": 0.025}
}

# Each market state changes how much money you make or lose
MARKET_STATES = {
    "up": 1.1,    # You gain 10%
    "down": 0.9,  # You lose 10%
    "flat": 1.0,  # No change
    "crash": 0.6, # You lose a lot
    "boom": 1.3,  # You gain a lot
}

# A Person has a personality and money. They can be active (invested) or not.
class Person:
    def __init__(self, personality):
        self.personality = personality  # What kind of risk they like
        self.value = 1000  # Everyone starts with $1000
        self.active = True  # They're in the market at the start

    def decide(self, market_state, market_index):
        # Decide whether to stay in or leave the market this year
        stay_prob = PERSONALITIES[self.personality]["stay_in_prob"].get(
            "down" if market_state == "crash" else market_state, 0.6)

        # If they're out of the market, maybe they'll get back in
        if not self.active:
            base_chance = 0.25
            if market_index < 0.8:
                base_chance += 0.25  # Market is low—good time to buy!
            elif market_index < 1.0:
                base_chance += 0.1
            if random.random() < base_chance:
                self.active = True  # Rejoin the market
        # If they're in, they might decide to leave based on the market
        elif self.active and random.random() > stay_prob:
            self.active = False

    def update_value(self, market_state):
        # If the person is still in the market, change their money value
        if self.active:
            self.value *= MARKET_STATES[market_state]

# This makes the market more likely to go down if fewer people are investing
def adjust_for_participation(transitions, active_ratio):
    adjusted = {}
    for state, probs in transitions.items():
        adjusted[state] = probs.copy()
        if active_ratio < 0.5:
            adjusted[state]["down"] += 0.05  # Less confidence
            adjusted[state]["up"] = max(0, adjusted[state]["up"] - 0.03)
            adjusted[state]["boom"] = max(0, adjusted[state]["boom"] - 0.01)
        # Normalize so the total is still 1.0
        total = sum(adjusted[state].values())
        for key in adjusted[state]:
            adjusted[state][key] /= total
    return adjusted

# Simulate one year in the market
def simulate_year(people, current_state, market_index):
    active_people = [p for p in people if p.active]
    active_ratio = len(active_people) / len(people)
    adjusted_transitions = adjust_for_participation(BASE_MARKOV_TRANSITIONS, active_ratio)

    # Choose next market state based on current one
    next_state = random.choices(
        population=list(adjusted_transitions[current_state].keys()),
        weights=list(adjusted_transitions[current_state].values()),
        k=1
    )[0]

    # Each person decides what to do and updates their money
    for person in people:
        person.decide(next_state, market_index)
        person.update_value(next_state)
    return next_state

# Make a bunch of people with random personalities
def generate_people(n):
    personality_types = list(PERSONALITIES.keys())
    return [Person(random.choice(personality_types)) for _ in range(n)]

# Create a summary of everyone's money
def generate_report(people):
    values = [round(p.value, 2) for p in people]
    if not values:
        return "No data."
    report = {
        "mean": round(statistics.mean(values), 2),
        "median": round(statistics.median(values), 2),
        "min": round(min(values), 2),
        "max": round(max(values), 2),
    }
    try:
        report["mode"] = round(statistics.mode(values), 2)
    except statistics.StatisticsError:
        report["mode"] = "No unique mode"
    return report

# Print out stats nicely for a group of people
def stats_report(group, name):
    values = [round(p.value, 2) for p in group]
    print(f"\n--- {name} Report ({len(values)} people) ---")
    if values:
        print(f"Mean: {round(statistics.mean(values), 2)}")
        print(f"Median: {round(statistics.median(values), 2)}")
        try:
            print(f"Mode: {round(statistics.mode(values), 2)}")
        except statistics.StatisticsError:
            print("Mode: No unique mode")
        print(f"Min: {min(values)}")
        print(f"Max: {max(values)}")
    else:
        print("No data to show.")

# ==== MAIN SIMULATION STARTS HERE ====
n = int(input("Enter number of people in the simulation: "))
people = generate_people(n)

year = 0
market_history = []
market_value_history = []
current_state = "flat"  # Start with a stable market
market_index = 1.0  # Starting point of market's value

# Run the simulation for 20 years
while year < 20:
    print(f"\nYear {year} - {year + 1} Simulation")
    interval = int(input("Enter number of years to simulate before update (1-20): "))
    if year + interval > 20:
        interval = 20 - year
        print(f"Adjusting to {interval} year(s) to stay within 20-year limit.")

    interval_states = []
    for _ in range(interval):
        current_state = simulate_year(people, current_state, market_index)
        market_index *= MARKET_STATES[current_state]
        market_history.append(current_state)
        market_value_history.append(sum(p.value for p in people if p.active))
        interval_states.append(current_state)
        year += 1

    # Show what happened in these years
    print("\nMarket update for this interval:")
    for i, state in enumerate(interval_states):
        print(f"Year {year - interval + i + 1}: {state.upper()}")

    # Show stats for people who stayed vs. left
    active_people = [p for p in people if p.active]
    inactive_people = [p for p in people if not p.active]

    stats_report(active_people, "Active Participants")
    stats_report(inactive_people, "Exited Participants")

# Final wrap-up after 20 years
print("\n\n==== FINAL SUMMARY ====")
stats_report([p for p in people if p.active], "Active Participants")
stats_report([p for p in people if not p.active], "Exited Participants")

# Plot a line graph of how the total market value changed over time
def plot_market_value(history):
    years = list(range(1, len(history) + 1))
    plt.plot(years, history, marker='o', color='green')
    plt.title("Total Market Value Over Time")
    plt.xlabel("Year")
    plt.ylabel("Total Active Investment Value")
    plt.grid(True)
    plt.show()

plot_market_value(market_value_history)
