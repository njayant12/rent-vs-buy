#!/usr/bin/env python3
"""
Down Payment: Monthly Contributions for 4 Years, Grow in Year 5, Sell

Realistic scenario:
1. Calculate monthly contribution needed to reach $410K after 4 years at 7%
2. Year 5: Let that $410K grow to $438.7K
3. Sell everything in year 5
4. Cost basis = sum of all monthly contributions (NOT $410K!)
5. Pay capital gains tax on (sale price - cost basis)

This is the REAL cost basis calculation.
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

def calculate_monthly_contribution_needed(target, months, annual_return):
    """Calculate monthly contribution needed to reach target with compound returns"""
    # Future Value of Annuity formula: FV = PMT * [((1 + r)^n - 1) / r]
    # Solving for PMT: PMT = FV / [((1 + r)^n - 1) / r]
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

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
print("DOWN PAYMENT: Monthly Contributions Over 4 Years, Grow in Year 5, Sell with Real Cost Basis")
print("=" * 100)
print()

# Step 1: Calculate monthly contribution needed to reach $410K after 4 years
months_saving = 48  # 4 years
monthly_contribution = calculate_monthly_contribution_needed(TOTAL_UPFRONT, months_saving, INVESTMENT_RETURN)

# Step 2: Calculate the actual cost basis (sum of contributions)
cost_basis = monthly_contribution * months_saving

print("STEP 1: Saving Phase (Years 1-4)")
print(f"  • Target after 4 years: ${TOTAL_UPFRONT:,.0f}")
print(f"  • Monthly contribution needed: ${monthly_contribution:,.0f}")
print(f"  • Total contributions (cost basis): ${cost_basis:,.0f}")
print(f"  • Portfolio value at end of Year 4: ${TOTAL_UPFRONT:,.0f}")
print(f"  • Gains during saving period: ${TOTAL_UPFRONT - cost_basis:,.0f}")
print()

# Step 3: Year 5 - let it grow
value_end_year5 = TOTAL_UPFRONT * (1 + INVESTMENT_RETURN)
gain_year5 = value_end_year5 - TOTAL_UPFRONT
total_gains = value_end_year5 - cost_basis

print("STEP 2: Growth Year (Year 5)")
print(f"  • Start of Year 5: ${TOTAL_UPFRONT:,.0f}")
print(f"  • Grows at 7% to: ${value_end_year5:,.0f}")
print(f"  • Gain in Year 5: ${gain_year5:,.0f}")
print()

# Step 4: Sell and calculate capital gains tax
print("STEP 3: Sale and Capital Gains Tax")
print(f"  • Sale price: ${value_end_year5:,.0f}")
print(f"  • Cost basis (contributions): ${cost_basis:,.0f}")
print(f"  • Total capital gain: ${total_gains:,.0f}")
print(f"  • Tax rate: {COMBINED_CAP_GAINS*100:.1f}% (15% federal + 9.3% CA)")

capital_gains_tax = total_gains * COMBINED_CAP_GAINS
after_tax_proceeds = value_end_year5 - capital_gains_tax

print(f"  • Tax owed: ${capital_gains_tax:,.0f}")
print(f"  • After-tax proceeds: ${after_tax_proceeds:,.0f}")
print()

# Step 5: Compare buyer vs renter
print("=" * 100)
print("COMPARISON: BUYER VS RENTER")
print("=" * 100)
print()
print("Buyer (sells and buys house):")
print(f"  • Sells portfolio, pays ${capital_gains_tax:,.0f} tax")
print(f"  • Has ${after_tax_proceeds:,.0f} after tax")
print(f"  • Uses ${TOTAL_UPFRONT:,.0f} for down payment")
print(f"  • Invests remaining ${after_tax_proceeds - TOTAL_UPFRONT:,.0f}")
print()
print("Renter (keeps investing):")
print(f"  • Doesn't sell, keeps all ${value_end_year5:,.0f} invested")
print(f"  • No tax event, no capital gains paid")
print()

# Step 6: Run 30-year analysis
result = run_30_year_analysis(
    buyer_starting_capital=after_tax_proceeds,
    renter_starting_capital=value_end_year5
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

# Compare to baseline
baseline_gap = 2_234_418  # Fresh RSUs scenario
extra_drag = abs(result['difference']) - baseline_gap

print("=" * 100)
print("DRAG ANALYSIS")
print("=" * 100)
print()
print(f"Baseline (Fresh RSUs, both start with ${TOTAL_UPFRONT:,.0f}):")
print(f"  Renting wins by ${baseline_gap:,.0f}")
print()
print(f"This Scenario (Monthly contributions, real cost basis):")
print(f"  Capital gains tax paid: ${capital_gains_tax:,.0f}")
print(f"  Renting wins by ${abs(result['difference']):,.0f}")
print(f"  Extra drag: ${extra_drag:,.0f}")
print()

# Breakdown
compounded_tax = capital_gains_tax * ((1 + INVESTMENT_RETURN) ** YEARS)

print("Why the drag:")
print(f"  • Buyer pays ${capital_gains_tax:,.0f} in tax upfront")
print(f"  • That ${capital_gains_tax:,.0f} compounds to ${compounded_tax:,.0f} over 30 years")
print(f"  • Actual drag: ${extra_drag:,.0f}")
print()

# Comparison table
print("=" * 100)
print("COMPARISON TO OTHER STRATEGIES")
print("=" * 100)
print()
print(f"{'Strategy':<60} {'Tax Paid':<15} {'30-Yr Drag':<15}")
print("-" * 100)
print(f"{'1. Fresh RSUs (baseline)':<60} ${0:>13,.0f} ${0:>13,.0f}")
print(f"{'2. Monthly contributions 4yr, grow 1yr, sell (THIS)':<60} ${capital_gains_tax:>13,.0f} ${extra_drag:>13,.0f}")
print(f"{'3. Accumulate $410K lump sum, grow 1yr, sell':<60} ${6_974:>13,.0f} ${56_605:>13,.0f}")
print(f"{'4. Lump sum 4yr ago, sell immediately':<60} ${25_067:>13,.0f} ${203_456:>13,.0f}")
print(f"{'5. Save in HYSA 4 years @ 3%':<60} {'$0':>13} ${547_834:>13,.0f}")
print()

print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()
print(f"When you save ${monthly_contribution:,.0f}/month for 4 years:")
print(f"  • Your cost basis is only ${cost_basis:,.0f} (what you contributed)")
print(f"  • By Year 4, it grows to ${TOTAL_UPFRONT:,.0f} (includes ${TOTAL_UPFRONT - cost_basis:,.0f} gains)")
print(f"  • By Year 5, it grows to ${value_end_year5:,.0f}")
print(f"  • Total gain: ${total_gains:,.0f} (on which you pay tax)")
print()
print(f"Tax impact:")
print(f"  • Tax on ${total_gains:,.0f} @ 24.3% = ${capital_gains_tax:,.0f}")
print(f"  • This is {capital_gains_tax / 6_974:.1f}x MORE than the '$410K lump sum' scenario")
print(f"  • Because you're paying tax on ALL gains (${total_gains:,.0f}), not just Year 5 (${gain_year5:,.0f})")
print()
print(f"The trade-off:")
print(f"  • WORSE than having a lump sum appear (${extra_drag:,.0f} vs ${56_605:,.0f})")
print(f"  • MUCH BETTER than HYSA (${extra_drag:,.0f} vs ${547_834:,.0f})")
print()

print("=" * 100)
