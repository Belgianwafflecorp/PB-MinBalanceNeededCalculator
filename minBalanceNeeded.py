# python min balance needed app

import json

# Ask user to paste the full JSON content
print("Paste the full JSON content (end input with an empty line):")
lines = []
while True:
    line = input()
    if line.strip() == "":  # Stop reading input on an empty line
        break
    lines.append(line)

# Combine lines into a single JSON string
config_str = "\n".join(lines)

try:
    # Parse the JSON content
    config = json.loads(config_str)
except json.JSONDecodeError as e:
    print("Invalid JSON input. Please ensure the content is valid JSON.")
    print(f"Error details: {e}")
    exit(1)

# Extract the "bot" -> "long" section from the JSON
long_config = config.get("bot", {}).get("long", {})
short_config = config.get("bot", {}).get("short", {})

# Extract values from the "long" section
entry_initial_qty_pct_long = long_config.get("entry_initial_qty_pct", 0.0)
twe_long = long_config.get("total_wallet_exposure_limit", 0.0)
n_pos_long = long_config.get("n_positions", 0)

# Extract values from the "short" section
entry_initial_qty_pct_short = short_config.get("entry_initial_qty_pct", 0.0)
twe_short = short_config.get("total_wallet_exposure_limit", 0.0)
n_pos_short = short_config.get("n_positions", 0)

# Ask user for manual input for min order size
print("min order size in $ of exchange: ", end="")
coinMinOrder = float(input())
print()

# Calculate min balance needed for long
try:
    minBalanceNeeded_long = coinMinOrder / entry_initial_qty_pct_long / twe_long * n_pos_long
    print("min balance needed for long: $", minBalanceNeeded_long)
except ZeroDivisionError:
    print("Error: Division by zero occurred in the long section. Please check the input values.")
    minBalanceNeeded_long = None

# Calculate min balance needed for short
try:
    minBalanceNeeded_short = coinMinOrder / entry_initial_qty_pct_short / twe_short * n_pos_short
    print("min balance needed for short: $", minBalanceNeeded_short)
except ZeroDivisionError:
    print("Error: Division by zero occurred in the short section. Please check the input values.")
    minBalanceNeeded_short = None

# Ask user for balance they want to use
print("balance you want to use: ", end="")
balance = float(input())
print()

# Calculate first order sizes for long
if minBalanceNeeded_long is not None:
    try:
        firstOrderSizeWithMinBalance_long = minBalanceNeeded_long * (twe_long / n_pos_long) * entry_initial_qty_pct_long
        print("first order size with minimum balance for long: $", firstOrderSizeWithMinBalance_long)

        firstOrderSize_long = balance * (twe_long / n_pos_long) * entry_initial_qty_pct_long
        print("first order size with your chosen balance for long: $", firstOrderSize_long)
    except ZeroDivisionError:
        print("Error: Division by zero occurred while calculating order sizes for long. Please check the input values.")

# Calculate first order sizes for short
if minBalanceNeeded_short is not None:
    try:
        firstOrderSizeWithMinBalance_short = minBalanceNeeded_short * (twe_short / n_pos_short) * entry_initial_qty_pct_short
        print("first order size with minimum balance for short: $", firstOrderSizeWithMinBalance_short)

        firstOrderSize_short = balance * (twe_short / n_pos_short) * entry_initial_qty_pct_short
        print("first order size with your chosen balance for short: $", firstOrderSize_short)
    except ZeroDivisionError:
        print("Error: Division by zero occurred while calculating order sizes for short. Please check the input values.")
