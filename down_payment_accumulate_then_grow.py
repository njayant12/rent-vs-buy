#!/usr/bin/env python3
"""
Down Payment Strategy: Accumulate $410K by Year 4, Grow in Year 5, Then Sell

Scenario:
- Save/invest over years 1-4 until you have $410K (cost basis)
- Year 5: Let it grow at 7% (no new contributions)
- End of Year 5: Sell everything and pay capital gains tax on ALL gains
- Use after-tax proceeds for down payment

Comparison:
- Buyer: Sells at end of year 5, pays capital gains tax
- Renter: Doesn't sell, keeps everything invested
"""

import sys
sys.path.append('/home/user/rent-vs-buy')

# Constants
PROPERTY_PRICE = 1_900_000
DOWN_PAYMENT_PCT = 0.20
CLOSING_COSTS = 30_000
TOTAL_UPFRONT = (PROPERTY_PRICE * DOWN_PAYMENT_PCT) + CLOSING_COSTS  # $410K

INITIAL_RENT = 5_800
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
RENT_INFLATION = 0.03
INSURANCE_INFLATION = 0.03
PROPERTY_TAX_INFLATION = 0.02
TAX_RATE = 0.413
MORTGAGE_RATE = 0.06
YEARS = 30

STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

# Capital gains tax (married filing jointly, $400K W2 income in CA)
LONG_TERM_CAP_GAINS_FEDERAL = 0.15
CA_STATE_TAX_ON_GAINS = 0.093
COMBINED_CAP_GAINS = LONG_TERM_CAP_GAINS_FEDERAL + CA_STATE_TAX_ON_GAINS  # 24.3%

def calculate_mortgage_payment(loan_amount):
    """Calculate monthly mortgage payment"""
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = 30 * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

def run_30_year_analysis(buyer_starting_capital, renter_starting_capital):
    """Run the 30-year rent vs buy analysis"""

    # Buyer setup
    loan_amount = PROPERTY_PRICE - (PROPERTY_PRICE * DOWN_PAYMENT_PCT)
    monthly_mortgage = calculate_mortgage_payment(loan_amount)

    buyer_investments = buyer_starting_capital - TOTAL_UPFRONT
    buyer_home_value = PROPERTY_PRICE
    buyer_mortgage_balance = loan_amount

    # Renter setup
    renter_investments = renter_starting_capital

    # Initial costs
    property_tax = PROPERTY_PRICE * 0.01
    home_insurance = 2_400

    for year in range(1, YEARS + 1):
        # Mortgage calculations
        annual_mortgage = monthly_mortgage * 12
        year_start_balance = buyer_mortgage_balance
        year_interest = 0
        temp_balance = year_start_balance

        for month in range(12):
            month_interest = temp_balance * (MORTGAGE_RATE / 12)
            month_principal = monthly_mortgage - month_interest
            year_interest += month_interest
            temp_balance -= month_principal

        year_principal = annual_mortgage - year_interest
        buyer_mortgage_balance = max(0, buyer_mortgage_balance - year_principal)

        # Tax benefit
        if loan_amount > MORTGAGE_INTEREST_CAP:
            deductible_interest = year_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
        else:
            deductible_interest = year_interest

        salt_deduction = min(property_tax, SALT_CAP)
        itemized = deductible_interest + salt_deduction
        excess = max(0, itemized - STANDARD_DEDUCTION)
        tax_savings = excess * TAX_RATE

        # After-tax costs
        costs_buyer_before_tax = annual_mortgage + property_tax + home_insurance
        costs_buyer_after_tax = costs_buyer_before_tax - tax_savings
        baseline_monthly_income = costs_buyer_after_tax / 12

        # Renter costs
        annual_rent = INITIAL_RENT * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        # Grow investments
        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

            buyer_investments = buyer_investments * (1 + monthly_investment_rate)

        # Home appreciation
        buyer_home_value = buyer_home_value * (1 + HOME_APPRECIATION)

        # Inflate costs
        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    # Final positions
    buyer_equity = buyer_home_value - buyer_mortgage_balance
    buyer_net_worth = buyer_investments + buyer_equity
    renter_net_worth = renter_investments

    return {
        'renter_final': renter_net_worth,
        'buyer_final': buyer_net_worth,
        'difference': renter_net_worth - buyer_net_worth
    }

print("=" * 100)
print("DOWN PAYMENT: Accumulate $410K by Year 4, Grow in Year 5, Sell and Pay Capital Gains")
print("=" * 100)
print()

# Scenario: You've saved up $410K in contributions by end of year 4
# This is your COST BASIS (the money you put in)
cost_basis = TOTAL_UPFRONT  # $410K

# In year 5, it grows at 7%
value_end_year5 = cost_basis * (1 + INVESTMENT_RETURN)  # $410K * 1.07 = $438.7K

# Capital gain
capital_gain = value_end_year5 - cost_basis  # $28.7K

# Tax on the gain
capital_gains_tax = capital_gain * COMBINED_CAP_GAINS  # $28.7K * 24.3% = $6,975

# After-tax proceeds
after_tax_proceeds = value_end_year5 - capital_gains_tax  # $438.7K - $7K = $431.7K

print("Setup:")
print(f"  • End of Year 4: You've saved/invested ${cost_basis:,.0f} (cost basis)")
print(f"  • Year 5: It grows at 7% to ${value_end_year5:,.0f}")
print(f"  • End of Year 5: You sell everything")
print()
print("Capital Gains Calculation:")
print(f"  • Cost basis (contributions): ${cost_basis:,.0f}")
print(f"  • Value at sale: ${value_end_year5:,.0f}")
print(f"  • Capital gain: ${capital_gain:,.0f}")
print(f"  • Tax rate: {COMBINED_CAP_GAINS*100:.1f}% (15% federal + 9.3% CA)")
print(f"  • Tax owed: ${capital_gains_tax:,.0f}")
print(f"  • After-tax proceeds: ${after_tax_proceeds:,.0f}")
print()

print("Comparison:")
print(f"  • Buyer: Sells, pays ${capital_gains_tax:,.0f} tax, has ${after_tax_proceeds:,.0f}")
print(f"           Uses ${TOTAL_UPFRONT:,.0f} for down payment, invests remaining ${after_tax_proceeds - TOTAL_UPFRONT:,.0f}")
print(f"  • Renter: Doesn't sell, keeps all ${value_end_year5:,.0f} invested (no tax event)")
print()

# Run the 30-year analysis
result = run_30_year_analysis(
    buyer_starting_capital=after_tax_proceeds,  # Buyer has after-tax proceeds
    renter_starting_capital=value_end_year5  # Renter has full amount (no tax)
)

print("=" * 100)
print("30-YEAR RENT VS BUY RESULTS")
print("=" * 100)
print()
print(f"Final Net Worth After 30 Years:")
print(f"  Renting: ${result['renter_final']:,.0f}")
print(f"  Buying:  ${result['buyer_final']:,.0f}")
print(f"  Gap:     ${abs(result['difference']):,.0f} (Renting wins)")
print()

# Compare to baseline (Fresh RSUs)
baseline_gap = 2_234_418  # From fresh RSUs scenario

extra_drag = abs(result['difference']) - baseline_gap
compounded_tax = capital_gains_tax * ((1 + INVESTMENT_RETURN) ** YEARS)

print("=" * 100)
print("DRAG ANALYSIS")
print("=" * 100)
print()
print(f"Baseline (Fresh RSUs, both start with ${TOTAL_UPFRONT:,.0f}):")
print(f"  Renting wins by ${baseline_gap:,.0f}")
print()
print(f"This Scenario (Accumulate by Y4, grow in Y5, sell):")
print(f"  Buyer pays ${capital_gains_tax:,.0f} in tax upfront")
print(f"  Renting wins by ${abs(result['difference']):,.0f}")
print(f"  Extra drag: ${extra_drag:,.0f}")
print()
print(f"Why the drag:")
print(f"  • Buyer starts with ${after_tax_proceeds:,.0f}")
print(f"  • Renter starts with ${value_end_year5:,.0f}")
print(f"  • Difference: ${value_end_year5 - after_tax_proceeds:,.0f} (the tax paid)")
print(f"  • That ${capital_gains_tax:,.0f} compounds to ${compounded_tax:,.0f} over 30 years")
print()

# Comparison to other strategies
print("=" * 100)
print("COMPARISON TO OTHER STRATEGIES")
print("=" * 100)
print()

print(f"{'Strategy':<55} {'Tax Paid':<15} {'30-Year Drag':<15}")
print("-" * 100)
print(f"{'1. Fresh RSUs (baseline)':<55} ${0:>13,.0f} ${0:>13,.0f}")
print(f"{'2. Accumulate $410K by Y4, grow in Y5, sell (THIS)':<55} ${capital_gains_tax:>13,.0f} ${extra_drag:>13,.0f}")
print(f"{'3. Save in HYSA 4 years @ 3%':<55} {'$0':>13} ${547_834:>13,.0f}")
print(f"{'4. Lump sum in stocks 4yr, sell immediately':<55} ${25_067:>13,.0f} ${203_456:>13,.0f}")
print()

print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()
print(f"By accumulating ${cost_basis:,.0f} over 4 years, then selling after 1 year of growth:")
print(f"  • You pay tax on only ${capital_gain:,.0f} of gains (the year 5 growth)")
print(f"  • Tax owed: ${capital_gains_tax:,.0f}")
print(f"  • 30-year drag: ${extra_drag:,.0f}")
print()
print(f"This is much better than:")
print(f"  • HYSA strategy: ${547_834:,.0f} drag (7.8x worse)")
print(f"  • Lump sum then sell: ${203_456:>,.0f} drag (2.9x worse)")
print()
print(f"But you have ${after_tax_proceeds - TOTAL_UPFRONT:,.0f} extra after paying for the down payment,")
print(f"which gives buyer a small boost compared to the baseline Fresh RSU scenario.")
print()

print("=" * 100)
