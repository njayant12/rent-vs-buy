#!/usr/bin/env python3
"""
After-Tax Return Comparison: HYSA vs Stocks

The KEY insight: We need to compare true after-tax returns, not nominal returns.

HYSA: 3% after-tax (already paid income tax on interest)
Stocks: 7% pre-tax, pay capital gains when sold

What's the EFFECTIVE after-tax return for stocks accounting for eventual cap gains?
"""

print("=" * 100)
print("AFTER-TAX RETURN COMPARISON: HYSA vs STOCKS")
print("=" * 100)
print()

# Tax rates
INCOME_TAX_RATE = 0.413  # 32% federal + 9.3% CA + 7.65% FICA
CAP_GAINS_RATE = 0.243   # 15% federal + 9.3% CA (no FICA)

# Returns
HYSA_NOMINAL = 0.045  # Assume 4.5% nominal HYSA rate
HYSA_AFTER_TAX = HYSA_NOMINAL * (1 - INCOME_TAX_RATE)  # Interest taxed as income

STOCK_RETURN = 0.07  # 7% growth, no tax until sale

print("=" * 100)
print("PART 1: UNDERSTANDING THE TAX TREATMENT")
print("=" * 100)
print()

print("HYSA (High-Yield Savings Account):")
print(f"  • Nominal rate: {HYSA_NOMINAL * 100:.1f}%")
print(f"  • Tax treatment: Interest taxed as ORDINARY INCOME")
print(f"  • Tax rate: {INCOME_TAX_RATE * 100:.1f}% (federal + state + FICA)")
print(f"  • After-tax return: {HYSA_AFTER_TAX * 100:.2f}%")
print()

print("Stocks (Brokerage Account):")
print(f"  • Nominal return: {STOCK_RETURN * 100:.1f}%")
print(f"  • Tax treatment: TAX-DEFERRED until sale, then CAPITAL GAINS")
print(f"  • Capital gains rate: {CAP_GAINS_RATE * 100:.1f}% (federal + state, no FICA)")
print(f"  • Effective after-tax return: Depends on holding period (calculated below)")
print()

print("KEY DIFFERENCE:")
print("  • HYSA: Pay income tax EVERY YEAR on interest (41.3% tax rate)")
print("  • Stocks: Pay capital gains ONCE when sold (24.3% tax rate, only on gains)")
print()

print("=" * 100)
print("PART 2: EFFECTIVE AFTER-TAX RETURN FOR STOCKS")
print("=" * 100)
print()

def calculate_effective_stock_return(years_held):
    """
    Calculate effective after-tax return for stocks held for N years

    Example: $100 invested
    - Grows at 7% for N years
    - Sell and pay capital gains tax
    - What was the effective after-tax annual return?
    """
    principal = 100
    value_before_tax = principal * ((1 + STOCK_RETURN) ** years_held)
    gain = value_before_tax - principal
    tax = gain * CAP_GAINS_RATE
    value_after_tax = value_before_tax - tax

    # Calculate effective annual return
    effective_annual_return = (value_after_tax / principal) ** (1 / years_held) - 1

    return {
        'years': years_held,
        'value_before_tax': value_before_tax,
        'gain': gain,
        'tax': tax,
        'value_after_tax': value_after_tax,
        'effective_return': effective_annual_return,
    }

print("If you invest $100 in stocks and hold for different periods:")
print()
print(f"{'Years':<10} {'Pre-Tax Value':<15} {'Tax Paid':<15} {'After-Tax Value':<15} {'Effective Annual Return':<25}")
print("-" * 100)

for years in [1, 4, 5, 10, 20, 30]:
    result = calculate_effective_stock_return(years)
    print(f"{result['years']:<10} ${result['value_before_tax']:>13,.2f} ${result['tax']:>13,.2f} ${result['value_after_tax']:>13,.2f} {result['effective_return']*100:>23.2f}%")

print()
print("KEY INSIGHT:")
print("  • The longer you hold stocks, the closer the effective after-tax return gets to 7%")
print("  • Why? The tax is paid once at the end, not every year")
print()

# Calculate for our scenarios
print("=" * 100)
print("PART 3: APPLYING TO OUR DOWN PAYMENT SCENARIOS")
print("=" * 100)
print()

# Scenario 1: HYSA for 5 years
print("SCENARIO 1: HYSA for 5 years")
print("-" * 100)

principal = 100
hysa_value = principal
for year in range(5):
    interest = hysa_value * HYSA_AFTER_TAX
    hysa_value += interest

print(f"  • Start: $100")
print(f"  • After-tax return: {HYSA_AFTER_TAX * 100:.2f}% per year")
print(f"  • End value: ${hysa_value:.2f}")
print(f"  • Total gain: ${hysa_value - principal:.2f}")
print()

# Scenario 2: Stocks for 5 years
print("SCENARIO 2: Stocks for 5 years (then sell)")
print("-" * 100)

stocks_5yr = calculate_effective_stock_return(5)

print(f"  • Start: $100")
print(f"  • Pre-tax return: {STOCK_RETURN * 100:.1f}% per year")
print(f"  • Pre-tax value: ${stocks_5yr['value_before_tax']:.2f}")
print(f"  • Capital gains tax: ${stocks_5yr['tax']:.2f}")
print(f"  • After-tax value: ${stocks_5yr['value_after_tax']:.2f}")
print(f"  • Effective after-tax return: {stocks_5yr['effective_return'] * 100:.2f}% per year")
print()

# Comparison
print("=" * 100)
print("PART 4: THE TRUE COMPARISON")
print("=" * 100)
print()

print("After 5 years, $100 becomes:")
print(f"  • HYSA: ${hysa_value:.2f} (at {HYSA_AFTER_TAX*100:.2f}% after-tax)")
print(f"  • Stocks: ${stocks_5yr['value_after_tax']:.2f} (at {stocks_5yr['effective_return']*100:.2f}% effective after-tax)")
print()
print(f"Difference: ${stocks_5yr['value_after_tax'] - hysa_value:.2f}")
print(f"Stocks advantage: {(stocks_5yr['value_after_tax'] / hysa_value - 1) * 100:.1f}%")
print()

return_difference = stocks_5yr['effective_return'] - HYSA_AFTER_TAX
print(f"Return differential: {return_difference * 100:.2f}% per year")
print(f"  • Stocks effective after-tax: {stocks_5yr['effective_return'] * 100:.2f}%")
print(f"  • HYSA after-tax: {HYSA_AFTER_TAX * 100:.2f}%")
print()

print("=" * 100)
print("PART 5: APPLYING TO $410K DOWN PAYMENT")
print("=" * 100)
print()

# Calculate for actual down payment scenarios
target = 410_000

# HYSA: How much to save monthly to reach $410K in 5 years at 2.64% after-tax
def calculate_monthly_contribution(target, months, annual_return):
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

monthly_hysa = calculate_monthly_contribution(target, 60, HYSA_AFTER_TAX)
monthly_stocks = calculate_monthly_contribution(target, 48, STOCK_RETURN)

print("To save $410K down payment:")
print()
print("HYSA Strategy (5 years):")
print(f"  • Monthly contribution: ${monthly_hysa:,.0f}")
print(f"  • After-tax return: {HYSA_AFTER_TAX * 100:.2f}%")
print(f"  • Total contributions: ${monthly_hysa * 60:,.0f}")
print(f"  • Grows to: ${target:,.0f}")
print()

print("Stocks Strategy (4 years save + 1 year grow):")
print(f"  • Monthly contribution: ${monthly_stocks:,.0f}")
print(f"  • Pre-tax return: {STOCK_RETURN * 100:.1f}%")
print(f"  • Total contributions: ${monthly_stocks * 48:,.0f}")
print(f"  • Value at Year 4: ${target:,.0f}")
print(f"  • Value at Year 5: ${target * (1 + STOCK_RETURN):,.0f}")
print()

# Calculate the advantage
cost_basis_stocks = monthly_stocks * 48
value_year5 = target * (1 + STOCK_RETURN)
gain_stocks = value_year5 - cost_basis_stocks
tax_stocks = gain_stocks * CAP_GAINS_RATE
after_tax_stocks = value_year5 - tax_stocks

# If they had kept in HYSA instead
cost_basis_hysa = monthly_hysa * 60
# What if those contributions went to stocks instead?
balance_if_stocks = 0
monthly_stock_rate = STOCK_RETURN / 12
for month in range(60):
    balance_if_stocks = balance_if_stocks * (1 + monthly_stock_rate) + monthly_hysa

gain_if_stocks = balance_if_stocks - cost_basis_hysa
tax_if_stocks = gain_if_stocks * CAP_GAINS_RATE
after_tax_if_stocks = balance_if_stocks - tax_if_stocks

print("=" * 100)
print("THE REAL OPPORTUNITY COST (Accounting for Taxes)")
print("=" * 100)
print()

print("HYSA Strategy:")
print(f"  • Final value: ${target:,.0f}")
print(f"  • Cost basis: ${cost_basis_hysa:,.0f}")
print(f"  • Gains: ${target - cost_basis_hysa:,.0f} (already taxed yearly)")
print()

print("If those HYSA contributions went to stocks instead:")
print(f"  • Would grow to: ${balance_if_stocks:,.0f}")
print(f"  • Cost basis: ${cost_basis_hysa:,.0f}")
print(f"  • Gains: ${gain_if_stocks:,.0f}")
print(f"  • Capital gains tax: ${tax_if_stocks:,.0f}")
print(f"  • After-tax value: ${after_tax_if_stocks:,.0f}")
print()

opportunity_cost = after_tax_if_stocks - target
print(f"TRUE OPPORTUNITY COST (after accounting for cap gains tax): ${opportunity_cost:,.0f}")
print()

print("This is the ACTUAL amount you lost by choosing HYSA:")
print(f"  • You ended with: ${target:,.0f}")
print(f"  • Could have had (after tax): ${after_tax_if_stocks:,.0f}")
print(f"  • Lost: ${opportunity_cost:,.0f}")
print()

print("=" * 100)
print("FINAL ANSWER")
print("=" * 100)
print()

print("The true comparison accounting for taxes:")
print()
print(f"1. HYSA: 3% after-tax return (interest taxed yearly at 41.3%)")
print(f"2. Stocks: {stocks_5yr['effective_return']*100:.2f}% effective after-tax return over 5 years")
print(f"           (tax-deferred growth, then 24.3% cap gains)")
print()
print(f"Return advantage: {(stocks_5yr['effective_return'] - HYSA_AFTER_TAX) * 100:.2f}% per year")
print()
print(f"On $410K down payment over 5 years:")
print(f"  • HYSA opportunity cost: ${opportunity_cost:,.0f} (after accounting for cap gains tax!)")
print(f"  • This is LESS than the ${44_054:,} I calculated before")
print(f"  • Why? Because if you used stocks, you'd pay ${tax_if_stocks:,.0f} in cap gains tax")
print()
print("The correct opportunity cost is the AFTER-TAX difference!")
print()

print("=" * 100)
