#!/usr/bin/env python3
"""
30-Year Rent vs Buy Analysis - CORRECT BASELINE
Baseline income = 3% down spending (changes each year)
3% down invests $0, others invest the difference
"""

# Constants
PROPERTY_PRICE = 1_900_000
MONTHLY_RENT_INITIAL = 5_800
STARTING_CAPITAL = 410_000
MORTGAGE_RATE = 0.06
PROPERTY_TAX_RATE = 0.012
HOME_INSURANCE_ANNUAL = 3_000
CLOSING_COSTS = 30_000
RENT_GROWTH = 0.03
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
TAX_RATE = 0.413
STANDARD_DEDUCTION = 31_500
MORTGAGE_INTEREST_CAP = 750_000
SALT_CAP = 10_000
PMI_RATE = 0.01

def calculate_monthly_mortgage_payment(principal, annual_rate, years=30):
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment

def calculate_year_mortgage_breakdown(principal_remaining, monthly_payment):
    monthly_rate = MORTGAGE_RATE / 12
    interest_paid = 0
    principal_paid = 0
    balance = principal_remaining

    for month in range(12):
        interest_this_month = balance * monthly_rate
        principal_this_month = monthly_payment - interest_this_month
        interest_paid += interest_this_month
        principal_paid += principal_this_month
        balance -= principal_this_month

    return interest_paid, principal_paid, balance

def calculate_investment_growth_with_contributions(starting_balance, monthly_contribution, months=12):
    monthly_rate = INVESTMENT_RETURN / 12
    balance = starting_balance

    for month in range(months):
        balance = balance * (1 + monthly_rate)
        balance += monthly_contribution

    return balance

def calculate_tax_benefit(mortgage_interest, property_tax, loan_amount):
    if loan_amount > MORTGAGE_INTEREST_CAP:
        deductible_interest = mortgage_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
    else:
        deductible_interest = mortgage_interest

    salt_deduction = min(property_tax, SALT_CAP)
    itemized = deductible_interest + salt_deduction
    excess = max(0, itemized - STANDARD_DEDUCTION)
    tax_savings = excess * TAX_RATE

    return tax_savings

# Initialize scenarios
down_3pct = PROPERTY_PRICE * 0.03
loan_3pct = PROPERTY_PRICE - down_3pct
monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)

upfront_3pct = down_3pct + CLOSING_COSTS
investment_3pct = STARTING_CAPITAL - upfront_3pct
mortgage_balance_3pct = loan_3pct

down_20pct = PROPERTY_PRICE * 0.20
loan_20pct = PROPERTY_PRICE - down_20pct
monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)

upfront_20pct = down_20pct + CLOSING_COSTS
investment_20pct = STARTING_CAPITAL - upfront_20pct
mortgage_balance_20pct = loan_20pct

investment_rent = STARTING_CAPITAL

# Track values
property_value = PROPERTY_PRICE
property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE
home_insurance = HOME_INSURANCE_ANNUAL
annual_rent = MONTHLY_RENT_INITIAL * 12

print("="*80)
print("30-YEAR NET WORTH COMPARISON")
print("Baseline: 3% down spending (changes yearly)")
print("="*80)
print(f"\nStarting Capital: ${STARTING_CAPITAL:,}")
print(f"Property Price: ${PROPERTY_PRICE:,}")
print(f"Home Appreciation: {HOME_APPRECIATION*100}%")
print(f"Investment Return: {INVESTMENT_RETURN*100}%")
print()

# Print header
print(f"{'Year':<6} {'Renting':>15} {'3% Down':>15} {'20% Down':>15} {'Baseline':>12} {'Rent $':>12} {'20% $':>12}")
print("="*95)

for year in range(1, 31):
    # Update property value and costs
    property_value = property_value * (1 + HOME_APPRECIATION)
    property_tax = property_tax * 1.02
    home_insurance = home_insurance * 1.03
    annual_rent = annual_rent * (1 + RENT_GROWTH)

    # 3% DOWN - Calculate costs (defines baseline income)
    interest_3, principal_3, mortgage_balance_3pct = calculate_year_mortgage_breakdown(
        mortgage_balance_3pct, monthly_payment_3pct)

    equity_pct_3 = (property_value - mortgage_balance_3pct) / PROPERTY_PRICE
    pmi_3_annual = 0 if equity_pct_3 >= 0.20 else PROPERTY_PRICE * PMI_RATE

    costs_3_before_tax = (monthly_payment_3pct * 12) + property_tax + home_insurance + pmi_3_annual
    tax_savings_3 = calculate_tax_benefit(interest_3, property_tax,
                                          loan_3pct if year == 1 else mortgage_balance_3pct)
    costs_3_after_tax = costs_3_before_tax - tax_savings_3

    # BASELINE INCOME = 3% down after-tax costs
    baseline_monthly_income = costs_3_after_tax / 12

    # 20% DOWN - Calculate costs
    interest_20, principal_20, mortgage_balance_20pct = calculate_year_mortgage_breakdown(
        mortgage_balance_20pct, monthly_payment_20pct)

    costs_20_before_tax = (monthly_payment_20pct * 12) + property_tax + home_insurance
    tax_savings_20 = calculate_tax_benefit(interest_20, property_tax,
                                           loan_20pct if year == 1 else mortgage_balance_20pct)
    costs_20_after_tax = costs_20_before_tax - tax_savings_20
    monthly_20_spending = costs_20_after_tax / 12

    # 20% down can invest the difference
    monthly_savings_20 = baseline_monthly_income - monthly_20_spending

    # RENTING - Calculate costs
    monthly_rent = annual_rent / 12

    # Renter can invest the difference
    monthly_savings_rent = baseline_monthly_income - monthly_rent

    # INVESTMENT GROWTH
    # 3% down invests $0 (spends all income)
    investment_3pct = calculate_investment_growth_with_contributions(investment_3pct, 0, 12)

    # 20% down invests monthly savings
    investment_20pct = calculate_investment_growth_with_contributions(
        investment_20pct, monthly_savings_20, 12)

    # Renter invests monthly savings
    investment_rent = calculate_investment_growth_with_contributions(
        investment_rent, monthly_savings_rent, 12)

    # CALCULATE NET WORTH
    home_equity_3 = property_value - mortgage_balance_3pct
    net_worth_3 = investment_3pct + home_equity_3

    home_equity_20 = property_value - mortgage_balance_20pct
    net_worth_20 = investment_20pct + home_equity_20

    net_worth_rent = investment_rent

    # Print year results
    print(f"{year:<6} ${net_worth_rent:>14,.0f} ${net_worth_3:>14,.0f} ${net_worth_20:>14,.0f} " +
          f"${baseline_monthly_income:>11,.0f} ${monthly_savings_rent:>11,.0f} ${monthly_savings_20:>11,.0f}")

print("="*95)

# Final summary
print(f"\nFINAL NET WORTH AFTER 30 YEARS:")
print(f"  Renting:   ${net_worth_rent:>14,.0f}")
print(f"  3% Down:   ${net_worth_3:>14,.0f}")
print(f"  20% Down:  ${net_worth_20:>14,.0f}")

winner = max(net_worth_rent, net_worth_3, net_worth_20)
if winner == net_worth_rent:
    print(f"\n  Winner: Renting (by ${net_worth_rent - max(net_worth_3, net_worth_20):,.0f})")
elif winner == net_worth_3:
    print(f"\n  Winner: 3% Down (by ${net_worth_3 - max(net_worth_rent, net_worth_20):,.0f})")
else:
    print(f"\n  Winner: 20% Down (by ${net_worth_20 - max(net_worth_rent, net_worth_3):,.0f})")

print(f"\nFINAL BREAKDOWN:")
print(f"\nRenting:")
print(f"  Investments: ${investment_rent:,.0f}")

print(f"\n3% Down:")
print(f"  Investments: ${investment_3pct:,.0f}")
print(f"  Home Equity: ${home_equity_3:,.0f}")

print(f"\n20% Down:")
print(f"  Investments: ${investment_20pct:,.0f}")
print(f"  Home Equity: ${home_equity_20:,.0f}")

print("\n" + "="*80)
print("NOTE: Baseline income = 3% down after-tax spending (changes yearly)")
print("3% down invests $0/month, others invest the difference")
print("="*80)
