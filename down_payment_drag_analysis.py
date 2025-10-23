#!/usr/bin/env python3
"""
Down Payment Drag Analysis: Impact of how you saved the down payment

Comparing different saving strategies for the $410K down payment needed for
the $1.9M SF house, and showing the final impact after 30 years.

Scenarios:
1. Baseline (Fresh RSUs): Money appears right before purchase, no opportunity cost
2. Saved in HYSA: Saved over 4 years at 3% after-tax
3. Saved in stocks: Saved over 4 years at 7%, then paid capital gains tax on sale

This shows the TOTAL COST of each saving strategy including both:
- The opportunity cost during the 4-year saving period
- The 30-year rent vs buy outcome
"""

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

# Capital gains tax (for married filing jointly, $400K W2 income in CA)
# At $400K income, you're in 15% federal long-term cap gains bracket
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
print("DOWN PAYMENT DRAG ANALYSIS: How Saving Strategy Affects Final Outcome")
print("=" * 100)
print()
print(f"Property: ${PROPERTY_PRICE:,} San Francisco")
print(f"Down Payment Needed: ${TOTAL_UPFRONT:,} (20% + closing)")
print(f"Assumptions: 3% home appreciation, 7% investment return")
print()

# SCENARIO 1: Baseline (Fresh RSUs - no opportunity cost)
print("\n" + "=" * 100)
print("SCENARIO 1: BASELINE - Fresh RSUs (No Opportunity Cost)")
print("=" * 100)
print()
print("Setup:")
print(f"  • RSUs vest right before home purchase")
print(f"  • After taxes, you have exactly ${TOTAL_UPFRONT:,}")
print(f"  • No opportunity cost - you wouldn't have had this money otherwise")
print()

baseline = run_30_year_analysis(
    buyer_starting_capital=TOTAL_UPFRONT,
    renter_starting_capital=TOTAL_UPFRONT
)

print("30-Year Results:")
print(f"  Renting: ${baseline['renter_final']:,.0f}")
print(f"  Buying:  ${baseline['buyer_final']:,.0f}")
print(f"  Gap:     ${abs(baseline['difference']):,.0f} (Renting wins)")
print()

# SCENARIO 2: Saved in HYSA over 4 years
print("\n" + "=" * 100)
print("SCENARIO 2: Saved in HYSA at 3% After-Tax Over 4 Years")
print("=" * 100)
print()

years_saving = 4
hysa_rate = 0.03
stock_rate = 0.07

# How much did you need to save 4 years ago to have $410K today?
initial_amount_hysa = TOTAL_UPFRONT / ((1 + hysa_rate) ** years_saving)

# What if you had invested in stocks instead?
amount_if_stocks = initial_amount_hysa * ((1 + stock_rate) ** years_saving)

# Opportunity cost during the 4-year saving period
opportunity_cost_4_years = amount_if_stocks - TOTAL_UPFRONT

print("Setup:")
print(f"  • 4 years ago, you had ${initial_amount_hysa:,.0f} to save")
print(f"  • Option A (HYSA at 3%): Grew to ${TOTAL_UPFRONT:,.0f}")
print(f"  • Option B (Stocks at 7%): Would have grown to ${amount_if_stocks:,.0f}")
print(f"  • Opportunity cost: ${opportunity_cost_4_years:,.0f}")
print()

# Buyer has HYSA money, Renter has what stocks would have been
hysa_result = run_30_year_analysis(
    buyer_starting_capital=TOTAL_UPFRONT,
    renter_starting_capital=amount_if_stocks
)

print("30-Year Results:")
print(f"  Renting: ${hysa_result['renter_final']:,.0f}")
print(f"  Buying:  ${hysa_result['buyer_final']:,.0f}")
print(f"  Gap:     ${abs(hysa_result['difference']):,.0f} (Renting wins)")
print()
print("Drag Analysis:")
print(f"  • Lost during 4-year saving: ${opportunity_cost_4_years:,.0f}")
print(f"  • Compounds to extra gap: ${abs(hysa_result['difference']) - abs(baseline['difference']):,.0f}")
print(f"  • Total drag vs baseline: ${abs(hysa_result['difference']) - abs(baseline['difference']):,.0f}")
print()

# SCENARIO 3: Saved in stocks over 4 years, then sold and paid capital gains tax
print("\n" + "=" * 100)
print("SCENARIO 3: Saved in Stocks Over 4 Years, Sold and Paid Capital Gains Tax")
print("=" * 100)
print()

# Work backwards: Need $410K after capital gains tax
# Let's say you started with amount X four years ago
# After 4 years at 7%, you have: X * (1.07^4)
# You sell, pay capital gains tax on the gain
# After tax, you have $410K

# This is complex because we need to know the cost basis
# Let's assume you saved it all at once 4 years ago (lump sum)
# Cost basis = initial amount
# Gain = final amount - cost basis
# Tax = gain * 24.3%
# After-tax = final amount - tax

# Need to solve: final_amount - (final_amount - cost_basis) * 0.243 = 410K
# Where final_amount = cost_basis * 1.07^4

# Let cost_basis = X
# final_amount = X * (1.07^4) = X * 1.3108
# tax = (X * 1.3108 - X) * 0.243 = X * 0.3108 * 0.243 = X * 0.0755
# after_tax = X * 1.3108 - X * 0.0755 = X * 1.2353

# 410K = X * 1.2353
# X = 410K / 1.2353

growth_factor = (1 + stock_rate) ** years_saving  # 1.3108
cost_basis_stocks = TOTAL_UPFRONT / (growth_factor - (growth_factor - 1) * COMBINED_CAP_GAINS)
value_before_tax = cost_basis_stocks * growth_factor
capital_gain = value_before_tax - cost_basis_stocks
capital_gains_tax = capital_gain * COMBINED_CAP_GAINS
after_tax_proceeds = value_before_tax - capital_gains_tax

print("Setup:")
print(f"  • 4 years ago, you saved ${cost_basis_stocks:,.0f} (lump sum)")
print(f"  • Invested in stocks at 7%, grew to ${value_before_tax:,.0f}")
print(f"  • Capital gain: ${capital_gain:,.0f}")
print(f"  • Capital gains tax (24.3%): ${capital_gains_tax:,.0f}")
print(f"  • After-tax proceeds: ${after_tax_proceeds:,.0f}")
print()

# Now compare: what if renter kept it all invested without selling?
renter_amount_stocks = value_before_tax  # Renter doesn't sell, no tax event

stocks_result = run_30_year_analysis(
    buyer_starting_capital=after_tax_proceeds,  # Buyer pays tax, gets less
    renter_starting_capital=renter_amount_stocks  # Renter keeps it all invested
)

print("30-Year Results:")
print(f"  Renting: ${stocks_result['renter_final']:,.0f}")
print(f"  Buying:  ${stocks_result['buyer_final']:,.0f}")
print(f"  Gap:     ${abs(stocks_result['difference']):,.0f} (Renting wins)")
print()
print("Drag Analysis:")
print(f"  • Capital gains tax paid: ${capital_gains_tax:,.0f}")
print(f"  • That tax compounds to: ${capital_gains_tax * ((1 + INVESTMENT_RETURN) ** YEARS):,.0f} over 30 years")
print(f"  • Total drag vs baseline: ${abs(stocks_result['difference']) - abs(baseline['difference']):,.0f}")
print()

# Summary table
print("\n" + "=" * 100)
print("SUMMARY: DOWN PAYMENT DRAG IMPACT ON FINAL NET WORTH")
print("=" * 100)
print()
print(f"{'Scenario':<50} {'Renting':<20} {'Buying':<20} {'Gap':<20} {'Drag vs Baseline'}")
print("-" * 100)

scenarios = [
    ("Baseline (Fresh RSUs)", baseline, 0),
    ("Saved in HYSA (4 years @ 3%)", hysa_result, abs(hysa_result['difference']) - abs(baseline['difference'])),
    ("Saved in Stocks (4 years @ 7%, paid cap gains)", stocks_result, abs(stocks_result['difference']) - abs(baseline['difference']))
]

for name, result, drag in scenarios:
    print(f"{name:<50} ${result['renter_final']:>18,.0f} ${result['buyer_final']:>18,.0f} ${abs(result['difference']):>18,.0f} ${drag:>18,.0f}")

print()
print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()

print(f"1. HYSA Savings (Most Conservative):")
print(f"   • Opportunity cost over 4 years: ${opportunity_cost_4_years:,.0f}")
print(f"   • This compounds to extra gap: ${abs(hysa_result['difference']) - abs(baseline['difference']):,.0f}")
print(f"   • Being conservative costs you ${abs(hysa_result['difference']) - abs(baseline['difference']):,.0f} over 30 years!")
print()

print(f"2. Stock Savings (Then Pay Tax):")
print(f"   • Capital gains tax hit: ${capital_gains_tax:,.0f}")
print(f"   • That tax grows to: ${capital_gains_tax * ((1 + INVESTMENT_RETURN) ** YEARS):,.0f} in lost opportunity")
print(f"   • Total drag vs baseline: ${abs(stocks_result['difference']) - abs(baseline['difference']):,.0f}")
print()

print("3. The Winner:")
best_scenario = min(scenarios, key=lambda x: x[2])
worst_scenario = max(scenarios, key=lambda x: x[2])
print(f"   • Best: {best_scenario[0]} (drag: ${best_scenario[2]:,.0f})")
print(f"   • Worst: {worst_scenario[0]} (drag: ${worst_scenario[2]:,.0f})")
print(f"   • Difference: ${worst_scenario[2] - best_scenario[2]:,.0f}")
print()

print("=" * 100)
print("THE BOTTOM LINE")
print("=" * 100)
print()
print("Down payment drag creates a ${:,.0f} swing between best and worst saving strategy!".format(
    worst_scenario[2] - best_scenario[2]
))
print()
print("If you're planning to buy in 4 years:")
print(f"  ✗ Saving in HYSA costs you ${abs(hysa_result['difference']) - abs(baseline['difference']):,.0f}")
print(f"  ✗ Saving in stocks (then paying cap gains tax) costs you ${abs(stocks_result['difference']) - abs(baseline['difference']):,.0f}")
print()
print("The least-bad option? Fresh RSUs that vest right before purchase (no opportunity cost).")
print()
print("=" * 100)
