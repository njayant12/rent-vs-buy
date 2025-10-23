#!/usr/bin/env python3
"""
20% Down Payment: HYSA 5 Years vs Stocks 4+1 Years

Compares two saving strategies for $410K down payment:
1. HYSA: Save monthly over 5 years at 3% after-tax
2. Stocks: Save monthly over 4 years at 7%, grow 1 year, then sell with cap gains tax

Which is better for the 20% down scenario?
"""

# Constants
PROPERTY_PRICE = 1_900_000
DOWN_PAYMENT_PCT = 0.20
CLOSING_COSTS = 30_000
TOTAL_UPFRONT = (PROPERTY_PRICE * DOWN_PAYMENT_PCT) + CLOSING_COSTS  # $410K

INITIAL_RENT = 5_800
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
HYSA_RETURN = 0.03
RENT_INFLATION = 0.03
INSURANCE_INFLATION = 0.03
PROPERTY_TAX_INFLATION = 0.02
TAX_RATE = 0.413
MORTGAGE_RATE = 0.06
YEARS = 30

STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

# Capital gains tax
LONG_TERM_CAP_GAINS_FEDERAL = 0.15
CA_STATE_TAX_ON_GAINS = 0.093
COMBINED_CAP_GAINS = LONG_TERM_CAP_GAINS_FEDERAL + CA_STATE_TAX_ON_GAINS

def calculate_mortgage_payment(loan_amount):
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = 30 * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

def calculate_monthly_contribution_needed(target, months, annual_return):
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

def run_30_year_analysis(buyer_starting_capital, renter_starting_capital):
    """Run the 30-year rent vs buy analysis"""

    loan_amount = PROPERTY_PRICE - (PROPERTY_PRICE * DOWN_PAYMENT_PCT)
    monthly_mortgage = calculate_mortgage_payment(loan_amount)

    buyer_investments = buyer_starting_capital - TOTAL_UPFRONT
    buyer_home_value = PROPERTY_PRICE
    buyer_mortgage_balance = loan_amount

    renter_investments = renter_starting_capital

    property_tax = PROPERTY_PRICE * 0.01
    home_insurance = 2_400

    for year in range(1, YEARS + 1):
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

        if loan_amount > MORTGAGE_INTEREST_CAP:
            deductible_interest = year_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
        else:
            deductible_interest = year_interest

        salt_deduction = min(property_tax, SALT_CAP)
        itemized = deductible_interest + salt_deduction
        excess = max(0, itemized - STANDARD_DEDUCTION)
        tax_savings = excess * TAX_RATE

        costs_buyer_before_tax = annual_mortgage + property_tax + home_insurance
        costs_buyer_after_tax = costs_buyer_before_tax - tax_savings
        baseline_monthly_income = costs_buyer_after_tax / 12

        annual_rent = INITIAL_RENT * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

            buyer_investments = buyer_investments * (1 + monthly_investment_rate)

        buyer_home_value = buyer_home_value * (1 + HOME_APPRECIATION)

        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    buyer_equity = buyer_home_value - buyer_mortgage_balance
    buyer_net_worth = buyer_investments + buyer_equity
    renter_net_worth = renter_investments

    return {
        'renter_final': renter_net_worth,
        'buyer_final': buyer_net_worth,
        'difference': renter_net_worth - buyer_net_worth
    }

print("=" * 100)
print("20% DOWN PAYMENT: HYSA 5 Years vs Stocks 4+1 Years")
print("=" * 100)
print()

# SCENARIO 1: HYSA over 5 years
print("\n" + "=" * 100)
print("SCENARIO 1: HYSA - Save Monthly Over 5 Years @ 3% After-Tax")
print("=" * 100)
print()

months_hysa = 60  # 5 years
monthly_hysa = calculate_monthly_contribution_needed(TOTAL_UPFRONT, months_hysa, HYSA_RETURN)
cost_basis_hysa = monthly_hysa * months_hysa

# What if they had invested in stocks instead?
# Calculate what stocks would have grown to with same monthly contributions
balance_stocks = 0
monthly_stock_rate = INVESTMENT_RETURN / 12
for month in range(months_hysa):
    balance_stocks = balance_stocks * (1 + monthly_stock_rate)
    balance_stocks += monthly_hysa

opportunity_cost_hysa = balance_stocks - TOTAL_UPFRONT

print("Saving Phase (5 years):")
print(f"  • Monthly contribution: ${monthly_hysa:,.0f}")
print(f"  • Total contributions: ${cost_basis_hysa:,.0f}")
print(f"  • HYSA @ 3%: Grows to ${TOTAL_UPFRONT:,.0f}")
print(f"  • Stocks @ 7%: Would have grown to ${balance_stocks:,.0f}")
print(f"  • Opportunity cost: ${opportunity_cost_hysa:,.0f}")
print()

# Buyer has HYSA amount, Renter has what stocks would have been
hysa_result = run_30_year_analysis(
    buyer_starting_capital=TOTAL_UPFRONT,
    renter_starting_capital=balance_stocks
)

print("30-Year Results:")
print(f"  • Renting: ${hysa_result['renter_final']:,.0f}")
print(f"  • Buying: ${hysa_result['buyer_final']:,.0f}")
print(f"  • Gap: ${abs(hysa_result['difference']):,.0f} (Renting wins)")
print()

# SCENARIO 2: Stocks 4 years + 1 year growth with capital gains
print("\n" + "=" * 100)
print("SCENARIO 2: STOCKS - Save 4 Years, Grow 1 Year, Sell with Capital Gains")
print("=" * 100)
print()

months_saving = 48  # 4 years
monthly_stocks = calculate_monthly_contribution_needed(TOTAL_UPFRONT, months_saving, INVESTMENT_RETURN)
cost_basis_stocks = monthly_stocks * months_saving

# Year 5 growth
value_end_year5 = TOTAL_UPFRONT * (1 + INVESTMENT_RETURN)
total_gains = value_end_year5 - cost_basis_stocks
capital_gains_tax = total_gains * COMBINED_CAP_GAINS
after_tax_proceeds = value_end_year5 - capital_gains_tax

print("Saving Phase (Years 1-4):")
print(f"  • Monthly contribution: ${monthly_stocks:,.0f}")
print(f"  • Total contributions (cost basis): ${cost_basis_stocks:,.0f}")
print(f"  • Portfolio at Year 4: ${TOTAL_UPFRONT:,.0f}")
print()
print("Growth Year (Year 5):")
print(f"  • Grows to: ${value_end_year5:,.0f}")
print(f"  • Total capital gain: ${total_gains:,.0f}")
print(f"  • Tax @ 24.3%: ${capital_gains_tax:,.0f}")
print(f"  • After-tax proceeds: ${after_tax_proceeds:,.0f}")
print()

stocks_result = run_30_year_analysis(
    buyer_starting_capital=after_tax_proceeds,
    renter_starting_capital=value_end_year5
)

print("30-Year Results:")
print(f"  • Renting: ${stocks_result['renter_final']:,.0f}")
print(f"  • Buying: ${stocks_result['buyer_final']:,.0f}")
print(f"  • Gap: ${abs(stocks_result['difference']):,.0f} (Renting wins)")
print()

# COMPARISON
print("\n" + "=" * 100)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 100)
print()
print(f"{'Metric':<45} {'HYSA (5 years)':<25} {'Stocks (4+1 years)':<25}")
print("-" * 100)
print(f"{'Monthly savings':<45} ${monthly_hysa:>23,.0f} ${monthly_stocks:>23,.0f}")
print(f"{'Total contributions (cost basis)':<45} ${cost_basis_hysa:>23,.0f} ${cost_basis_stocks:>23,.0f}")
print(f"{'Value at purchase time':<45} ${TOTAL_UPFRONT:>23,.0f} ${value_end_year5:>23,.0f}")
print(f"{'Capital gains tax paid':<45} ${0:>23,.0f} ${capital_gains_tax:>23,.0f}")
print(f"{'Buyer starting capital':<45} ${TOTAL_UPFRONT:>23,.0f} ${after_tax_proceeds:>23,.0f}")
print(f"{'Renter starting capital':<45} ${balance_stocks:>23,.0f} ${value_end_year5:>23,.0f}")
print()
print(f"{'Final net worth (Renting)':<45} ${hysa_result['renter_final']:>23,.0f} ${stocks_result['renter_final']:>23,.0f}")
print(f"{'Final net worth (Buying)':<45} ${hysa_result['buyer_final']:>23,.0f} ${stocks_result['buyer_final']:>23,.0f}")
print(f"{'Gap (Renting wins by)':<45} ${abs(hysa_result['difference']):>23,.0f} ${abs(stocks_result['difference']):>23,.0f}")
print()

# Analysis
baseline_gap = 2_234_418  # Fresh RSUs scenario
hysa_drag = abs(hysa_result['difference']) - baseline_gap
stocks_drag = abs(stocks_result['difference']) - baseline_gap

print("\n" + "=" * 100)
print("DRAG ANALYSIS (vs Fresh RSUs Baseline)")
print("=" * 100)
print()
print(f"Baseline (Fresh RSUs): Renting wins by ${baseline_gap:,.0f}")
print()
print(f"HYSA Strategy:")
print(f"  • Gap: ${abs(hysa_result['difference']):,.0f}")
print(f"  • Drag: ${hysa_drag:,.0f}")
print(f"  • Lost ${opportunity_cost_hysa:,.0f} by using HYSA instead of stocks")
print()
print(f"Stocks Strategy:")
print(f"  • Gap: ${abs(stocks_result['difference']):,.0f}")
print(f"  • Drag: ${stocks_drag:,.0f}")
print(f"  • Paid ${capital_gains_tax:,.0f} in capital gains tax")
print()

print("\n" + "=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()

print("1. MONTHLY SAVINGS COMPARISON:")
print(f"   • HYSA (5 years): ${monthly_hysa:,.0f}/month")
print(f"   • Stocks (4 years): ${monthly_stocks:,.0f}/month")
print(f"   • Stocks requires {monthly_stocks / monthly_hysa:.1f}x more monthly savings!")
print(f"   • But you save for 1 fewer year")
print()

print("2. OPPORTUNITY COST vs TAX COST:")
print(f"   • HYSA: Lost ${opportunity_cost_hysa:,.0f} in opportunity cost (no tax paid)")
print(f"   • Stocks: Paid ${capital_gains_tax:,.0f} in capital gains tax")
print(f"   • HYSA opportunity cost is {opportunity_cost_hysa / capital_gains_tax:.1f}x larger!")
print()

print("3. FINAL OUTCOME:")
print(f"   • HYSA: Renting wins by ${abs(hysa_result['difference']):,.0f}")
print(f"   • Stocks: Renting wins by ${abs(stocks_result['difference']):,.0f}")
print(f"   • HYSA is ${abs(hysa_result['difference']) - abs(stocks_result['difference']):,.0f} worse!")
print()

print("4. DRAG COMPARISON:")
print(f"   • HYSA drag: ${hysa_drag:,.0f}")
print(f"   • Stocks drag: ${stocks_drag:,.0f}")
print(f"   • HYSA creates {hysa_drag / stocks_drag:.1f}x more drag!")
print()

print("=" * 100)
print("THE BOTTOM LINE")
print("=" * 100)
print()
print("For 20% down payment ($410K):")
print()
print("HYSA Strategy (5 years @ 3%):")
print(f"  • Monthly: ${monthly_hysa:,.0f} (lower)")
print(f"  • Save for: 5 years (longer)")
print(f"  • Tax paid: $0")
print(f"  • Opportunity cost: ${opportunity_cost_hysa:,.0f}")
print(f"  ✗ Total drag: ${hysa_drag:,.0f} (MUCH WORSE)")
print()
print("Stocks Strategy (4 years save + 1 year grow @ 7%):")
print(f"  • Monthly: ${monthly_stocks:,.0f} (higher)")
print(f"  • Save for: 4 years (shorter)")
print(f"  • Tax paid: ${capital_gains_tax:,.0f}")
print(f"  • Opportunity cost: $0")
print(f"  ✓ Total drag: ${stocks_drag:,.0f} (MUCH BETTER)")
print()
print(f"Even though stocks require {monthly_stocks / monthly_hysa:.1f}x more monthly savings,")
print(f"the HYSA opportunity cost (${opportunity_cost_hysa:,.0f}) is {opportunity_cost_hysa / capital_gains_tax:.1f}x larger")
print(f"than the capital gains tax (${capital_gains_tax:,.0f}).")
print()
print(f"HYSA creates ${abs(hysa_result['difference']) - abs(stocks_result['difference']):,.0f} more drag over 30 years!")
print()
print("=" * 100)
