#!/usr/bin/env python3
"""
Simplified Analysis: Renting vs 20% Down Only
Baseline = Higher of the two costs (20% down is higher)
The one with lower costs invests the difference
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

print("="*90)
print("SIMPLIFIED ANALYSIS: RENTING vs 20% DOWN")
print("Baseline = Higher cost scenario (20% down buyer)")
print("="*90)

# Initialize
down_20pct = PROPERTY_PRICE * 0.20
loan_20pct = PROPERTY_PRICE - down_20pct
monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)

investment_20pct = STARTING_CAPITAL - down_20pct - CLOSING_COSTS
mortgage_balance_20pct = loan_20pct

investment_rent = STARTING_CAPITAL

property_value = PROPERTY_PRICE
property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE
home_insurance = HOME_INSURANCE_ANNUAL
annual_rent = MONTHLY_RENT_INITIAL * 12

print(f"\nSTARTING CAPITAL: ${STARTING_CAPITAL:,}")
print(f"Property Price: ${PROPERTY_PRICE:,}")
print(f"Home Appreciation: {HOME_APPRECIATION*100}%")
print(f"Investment Return: {INVESTMENT_RETURN*100}%")

print(f"\n20% DOWN SETUP:")
print(f"  Down Payment: ${down_20pct:,}")
print(f"  Closing Costs: ${CLOSING_COSTS:,}")
print(f"  Remaining to Invest: ${investment_20pct:,.0f}")
print(f"  Loan Amount: ${loan_20pct:,}")

print(f"\nRENTING SETUP:")
print(f"  Starting Capital (all invested): ${STARTING_CAPITAL:,}")
print(f"  Initial Rent: ${MONTHLY_RENT_INITIAL:,}/month")

print(f"\n{'='*90}")
print(f"{'Year':<6} {'Renting':>15} {'20% Down':>15} {'Baseline':>12} {'Rent Cost':>12} {'20% Cost':>12} {'Rent Invests':>14}")
print("="*90)

for year in range(1, 31):
    # Update values
    property_value = property_value * (1 + HOME_APPRECIATION)
    property_tax = property_tax * 1.02
    home_insurance = home_insurance * 1.03
    annual_rent = annual_rent * (1 + RENT_GROWTH)

    # 20% DOWN - Calculate after-tax costs
    interest_20, principal_20, mortgage_balance_20pct = calculate_year_mortgage_breakdown(
        mortgage_balance_20pct, monthly_payment_20pct)

    costs_20_before_tax = (monthly_payment_20pct * 12) + property_tax + home_insurance
    tax_savings_20 = calculate_tax_benefit(interest_20, property_tax,
                                           loan_20pct if year == 1 else mortgage_balance_20pct)
    costs_20_after_tax = costs_20_before_tax - tax_savings_20
    monthly_20_cost = costs_20_after_tax / 12

    # RENTING - Calculate costs
    monthly_rent = annual_rent / 12

    # BASELINE = Higher of the two (20% down is always higher)
    baseline_monthly = max(monthly_20_cost, monthly_rent)

    # Calculate monthly savings
    monthly_savings_20 = baseline_monthly - monthly_20_cost  # Will be $0 (20% down IS the baseline)
    monthly_savings_rent = baseline_monthly - monthly_rent

    # INVESTMENT GROWTH
    # 20% down invests $0 (sets the baseline)
    investment_20pct = calculate_investment_growth_with_contributions(investment_20pct, 0, 12)

    # Renter invests the difference
    investment_rent = calculate_investment_growth_with_contributions(
        investment_rent, monthly_savings_rent, 12)

    # NET WORTH
    home_equity_20 = property_value - mortgage_balance_20pct
    net_worth_20 = investment_20pct + home_equity_20

    net_worth_rent = investment_rent

    # Print year results
    print(f"{year:<6} ${net_worth_rent:>14,.0f} ${net_worth_20:>14,.0f} " +
          f"${baseline_monthly:>11,.0f} ${monthly_rent:>11,.0f} ${monthly_20_cost:>11,.0f} " +
          f"${monthly_savings_rent:>13,.0f}")

print("="*90)

# Final summary
print(f"\nFINAL NET WORTH AFTER 30 YEARS:")
print(f"  Renting:   ${net_worth_rent:>14,.0f}")
print(f"  20% Down:  ${net_worth_20:>14,.0f}")

gap = net_worth_rent - net_worth_20
print(f"\n  {'Renting wins' if gap > 0 else '20% Down wins'} by ${abs(gap):,.0f}")

print(f"\nFINAL BREAKDOWN:")
print(f"\nRenting:")
print(f"  Investments: ${investment_rent:,.0f}")
print(f"  Home Equity: $0")

print(f"\n20% Down:")
print(f"  Investments: ${investment_20pct:,.0f}")
print(f"  Home Equity: ${home_equity_20:,.0f}")
print(f"  Property Value: ${property_value:,.0f}")
print(f"  Mortgage Balance: ${mortgage_balance_20pct:,.0f}")

print("\n" + "="*90)
print("KEY INSIGHT:")
print("="*90)
print("\nThis model assumes:")
print("  - Both scenarios have same income (matched to 20% down costs)")
print("  - 20% down buyer spends all income → invests $0")
print("  - Renter has lower costs → invests the difference")
print("\nThis is the SIMPLEST comparison:")
print("  'What if I had enough income to afford the 20% down house?'")
print("  'Should I rent instead and invest the savings?'")
print("="*90)
