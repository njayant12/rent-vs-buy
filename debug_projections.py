#!/usr/bin/env python3
"""
Debug Rent vs Buy Projections - Years 1 & 2
Parameters:
- 3% rent growth
- 20% down payment in SF
- Starting capital: $410K
- Property price: $1.9M
"""

# Constants
PROPERTY_PRICE = 1_900_000
MONTHLY_RENT = 5_800
DOWN_PAYMENT_PCT = 0.20
STARTING_CAPITAL = 410_000
MORTGAGE_RATE = 0.06
PROPERTY_TAX_RATE = 0.012
HOME_INSURANCE = 3_000
CLOSING_COSTS = 30_000
RENT_GROWTH = 0.03
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
TAX_RATE = 0.413  # 32% federal + 9.3% CA
STANDARD_DEDUCTION = 31_500  # Married
MORTGAGE_INTEREST_CAP = 750_000
SALT_CAP = 10_000

def calculate_monthly_mortgage_payment(principal, annual_rate, years=30):
    """Calculate monthly P&I payment"""
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment

def calculate_year_mortgage_breakdown(principal_remaining, annual_payment):
    """Calculate interest and principal for a given year"""
    monthly_rate = MORTGAGE_RATE / 12
    interest_paid = 0
    principal_paid = 0
    balance = principal_remaining
    monthly_payment = annual_payment / 12

    for month in range(12):
        interest_this_month = balance * monthly_rate
        principal_this_month = monthly_payment - interest_this_month
        interest_paid += interest_this_month
        principal_paid += principal_this_month
        balance -= principal_this_month

    return interest_paid, principal_paid, balance

print("="*80)
print("RENT VS BUY ANALYSIS - YEAR 1 & 2 DETAILED BREAKDOWN")
print("="*80)
print(f"\nSTARTING PARAMETERS:")
print(f"  Property Price: ${PROPERTY_PRICE:,}")
print(f"  Monthly Rent: ${MONTHLY_RENT:,}")
print(f"  Starting Capital: ${STARTING_CAPITAL:,}")
print(f"  Down Payment: {DOWN_PAYMENT_PCT*100}%")
print(f"  Mortgage Rate: {MORTGAGE_RATE*100}%")
print(f"  Home Appreciation: {HOME_APPRECIATION*100}%")
print(f"  Rent Growth: {RENT_GROWTH*100}%")
print(f"  Investment Return: {INVESTMENT_RETURN*100}%")
print()

# BUYING SCENARIO
print("="*80)
print("BUYING SCENARIO (20% DOWN)")
print("="*80)

down_payment = PROPERTY_PRICE * DOWN_PAYMENT_PCT
loan_amount = PROPERTY_PRICE - down_payment
total_upfront = down_payment + CLOSING_COSTS
uninvested_capital = STARTING_CAPITAL - total_upfront

print(f"\nUPFRONT COSTS:")
print(f"  Down Payment (20%): ${down_payment:,.0f}")
print(f"  Closing Costs: ${CLOSING_COSTS:,}")
print(f"  Total Upfront: ${total_upfront:,.0f}")
print(f"  Remaining to Invest: ${uninvested_capital:,.0f}")
print(f"  Loan Amount: ${loan_amount:,.0f}")

# Monthly mortgage payment
monthly_payment = calculate_monthly_mortgage_payment(loan_amount, MORTGAGE_RATE)
annual_mortgage = monthly_payment * 12

print(f"\nMORTGAGE:")
print(f"  Monthly P&I Payment: ${monthly_payment:,.2f}")
print(f"  Annual P&I Payment: ${annual_mortgage:,.2f}")

# Year 1 - Buying
print("\n" + "="*80)
print("YEAR 1 - BUYING")
print("="*80)

property_value_y1 = PROPERTY_PRICE * (1 + HOME_APPRECIATION)
appreciation_y1 = property_value_y1 - PROPERTY_PRICE

interest_y1, principal_y1, balance_y1 = calculate_year_mortgage_breakdown(loan_amount, annual_mortgage)
property_tax_y1 = PROPERTY_PRICE * PROPERTY_TAX_RATE

# Tax calculation
deductible_interest = min(interest_y1, (MORTGAGE_INTEREST_CAP / loan_amount) * interest_y1)
salt_deduction = min(property_tax_y1, SALT_CAP)
itemized_deductions = deductible_interest + salt_deduction
excess_deductions = max(0, itemized_deductions - STANDARD_DEDUCTION)
tax_savings_y1 = excess_deductions * TAX_RATE

# Total costs
total_costs_y1 = annual_mortgage + property_tax_y1 + HOME_INSURANCE
net_costs_y1 = total_costs_y1 - tax_savings_y1

# Investment returns on uninvested capital
investment_returns_y1 = uninvested_capital * INVESTMENT_RETURN

print(f"\n1. HOME APPRECIATION:")
print(f"   Property Value Start: ${PROPERTY_PRICE:,}")
print(f"   Property Value End: ${property_value_y1:,.0f}")
print(f"   Appreciation (3%): ${appreciation_y1:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid Year 1: ${principal_y1:,.0f}")
print(f"   Mortgage Balance Start: ${loan_amount:,}")
print(f"   Mortgage Balance End: ${balance_y1:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Uninvested Capital: ${uninvested_capital:,.0f}")
print(f"   Investment Return (7%): ${investment_returns_y1:,.0f}")

print(f"\n4. COSTS:")
print(f"   Mortgage P&I: ${annual_mortgage:,.0f}")
print(f"   Property Tax: ${property_tax_y1:,.0f}")
print(f"   Home Insurance: ${HOME_INSURANCE:,}")
print(f"   Total Costs (before tax): ${total_costs_y1:,.0f}")

print(f"\n5. TAX BENEFIT:")
print(f"   Mortgage Interest Paid: ${interest_y1:,.0f}")
print(f"   Deductible Interest (capped): ${deductible_interest:,.0f}")
print(f"   Property Tax: ${property_tax_y1:,.0f}")
print(f"   SALT Deduction (capped at $10k): ${salt_deduction:,.0f}")
print(f"   Total Itemized: ${itemized_deductions:,.0f}")
print(f"   Standard Deduction: ${STANDARD_DEDUCTION:,}")
print(f"   Excess Deductions: ${excess_deductions:,.0f}")
print(f"   Tax Savings (41.3%): ${tax_savings_y1:,.0f}")

print(f"\n6. NET POSITION YEAR 1:")
print(f"   Home Appreciation: +${appreciation_y1:,.0f}")
print(f"   Home Equity (principal): +${principal_y1:,.0f}")
print(f"   Investment Returns: +${investment_returns_y1:,.0f}")
print(f"   Net Costs (after tax): -${net_costs_y1:,.0f}")
print(f"   Closing Costs (one-time): -${CLOSING_COSTS:,}")
print(f"   -------------------------------------------------------")
total_net_y1 = appreciation_y1 + principal_y1 + investment_returns_y1 - net_costs_y1 - CLOSING_COSTS
print(f"   TOTAL NET YEAR 1: ${total_net_y1:,.0f}")

# Year 2 - Buying
print("\n" + "="*80)
print("YEAR 2 - BUYING")
print("="*80)

property_value_y2 = property_value_y1 * (1 + HOME_APPRECIATION)
appreciation_y2 = property_value_y2 - property_value_y1

interest_y2, principal_y2, balance_y2 = calculate_year_mortgage_breakdown(balance_y1, annual_mortgage)
property_tax_y2 = property_tax_y1 * 1.02  # 2% annual increase

# Tax calculation
deductible_interest_y2 = min(interest_y2, (MORTGAGE_INTEREST_CAP / balance_y1) * interest_y2)
salt_deduction_y2 = min(property_tax_y2, SALT_CAP)
itemized_deductions_y2 = deductible_interest_y2 + salt_deduction_y2
excess_deductions_y2 = max(0, itemized_deductions_y2 - STANDARD_DEDUCTION)
tax_savings_y2 = excess_deductions_y2 * TAX_RATE

# Total costs
home_insurance_y2 = HOME_INSURANCE * (1.03)  # 3% inflation
total_costs_y2 = annual_mortgage + property_tax_y2 + home_insurance_y2
net_costs_y2 = total_costs_y2 - tax_savings_y2

# Investment returns (compounded)
uninvested_capital_y2 = uninvested_capital * (1 + INVESTMENT_RETURN)
new_returns_y2 = uninvested_capital_y2 * INVESTMENT_RETURN
cumulative_investment_y2 = uninvested_capital_y2 + new_returns_y2

print(f"\n1. HOME APPRECIATION:")
print(f"   Property Value Start: ${property_value_y1:,.0f}")
print(f"   Property Value End: ${property_value_y2:,.0f}")
print(f"   Appreciation Year 2: ${appreciation_y2:,.0f}")
print(f"   Cumulative Appreciation: ${property_value_y2 - PROPERTY_PRICE:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid Year 2: ${principal_y2:,.0f}")
print(f"   Cumulative Principal: ${principal_y1 + principal_y2:,.0f}")
print(f"   Mortgage Balance Start: ${balance_y1:,.0f}")
print(f"   Mortgage Balance End: ${balance_y2:,.0f}")
print(f"   Total Home Equity: ${property_value_y2 - balance_y2:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Investment Balance Start Year 2: ${uninvested_capital_y2:,.0f}")
print(f"   Investment Return Year 2 (7%): ${new_returns_y2:,.0f}")
print(f"   Total Investment Value: ${cumulative_investment_y2:,.0f}")

print(f"\n4. COSTS:")
print(f"   Mortgage P&I: ${annual_mortgage:,.0f}")
print(f"   Property Tax: ${property_tax_y2:,.0f}")
print(f"   Home Insurance: ${home_insurance_y2:,.0f}")
print(f"   Total Costs (before tax): ${total_costs_y2:,.0f}")

print(f"\n5. TAX BENEFIT:")
print(f"   Mortgage Interest Paid: ${interest_y2:,.0f}")
print(f"   Deductible Interest: ${deductible_interest_y2:,.0f}")
print(f"   Property Tax: ${property_tax_y2:,.0f}")
print(f"   SALT Deduction: ${salt_deduction_y2:,.0f}")
print(f"   Tax Savings: ${tax_savings_y2:,.0f}")

print(f"\n6. NET POSITION YEAR 2:")
print(f"   Home Appreciation (Year 2): +${appreciation_y2:,.0f}")
print(f"   Home Equity (principal Year 2): +${principal_y2:,.0f}")
print(f"   Investment Returns (Year 2): +${new_returns_y2:,.0f}")
print(f"   Net Costs (after tax): -${net_costs_y2:,.0f}")
print(f"   -------------------------------------------------------")
total_net_y2 = appreciation_y2 + principal_y2 + new_returns_y2 - net_costs_y2
print(f"   TOTAL NET YEAR 2: ${total_net_y2:,.0f}")

# RENTING SCENARIO
print("\n" + "="*80)
print("RENTING SCENARIO")
print("="*80)

investment_capital_rent = STARTING_CAPITAL
investment_y1_rent = investment_capital_rent * INVESTMENT_RETURN
rent_y1 = MONTHLY_RENT * 12

print(f"\nYEAR 1 - RENTING:")
print(f"  Starting Capital: ${investment_capital_rent:,}")
print(f"  Investment Returns (7%): ${investment_y1_rent:,.0f}")
print(f"  Rent Paid: -${rent_y1:,}")
print(f"  Net Year 1: ${investment_y1_rent - rent_y1:,.0f}")

investment_capital_y2_rent = (investment_capital_rent + investment_y1_rent)
investment_y2_rent = investment_capital_y2_rent * INVESTMENT_RETURN
rent_y2 = rent_y1 * (1 + RENT_GROWTH)

print(f"\nYEAR 2 - RENTING:")
print(f"  Investment Balance Start: ${investment_capital_y2_rent:,.0f}")
print(f"  Investment Returns (7%): ${investment_y2_rent:,.0f}")
print(f"  Rent Paid: -${rent_y2:,.0f}")
print(f"  Net Year 2: ${investment_y2_rent - rent_y2:,.0f}")

# COMPARISON
print("\n" + "="*80)
print("COMPARISON SUMMARY")
print("="*80)

print(f"\nYEAR 1:")
print(f"  Renting Net: ${investment_y1_rent - rent_y1:,.0f}")
print(f"  Buying Net: ${total_net_y1:,.0f}")
print(f"  Difference: ${(total_net_y1 - (investment_y1_rent - rent_y1)):,.0f} " +
      ("(Buying wins)" if total_net_y1 > investment_y1_rent - rent_y1 else "(Renting wins)"))

print(f"\nYEAR 2:")
print(f"  Renting Net: ${investment_y2_rent - rent_y2:,.0f}")
print(f"  Buying Net: ${total_net_y2:,.0f}")
print(f"  Difference: ${(total_net_y2 - (investment_y2_rent - rent_y2)):,.0f} " +
      ("(Buying wins)" if total_net_y2 > investment_y2_rent - rent_y2 else "(Renting wins)"))

print(f"\nCUMULATIVE 2-YEAR:")
cumulative_rent = (investment_y1_rent - rent_y1) + (investment_y2_rent - rent_y2)
cumulative_buy = total_net_y1 + total_net_y2
print(f"  Renting Cumulative: ${cumulative_rent:,.0f}")
print(f"  Buying Cumulative: ${cumulative_buy:,.0f}")
print(f"  Difference: ${(cumulative_buy - cumulative_rent):,.0f} " +
      ("(Buying wins)" if cumulative_buy > cumulative_rent else "(Renting wins)"))

# NET WORTH POSITIONS
print("\n" + "="*80)
print("NET WORTH AFTER 2 YEARS")
print("="*80)

print(f"\nRENTING:")
renting_cash = investment_capital_rent + investment_y1_rent - rent_y1 + investment_y2_rent - rent_y2
print(f"  Cash/Investments: ${renting_cash:,.0f}")
print(f"  Home Equity: $0")
print(f"  Total Net Worth: ${renting_cash:,.0f}")

print(f"\nBUYING:")
buying_home_equity = property_value_y2 - balance_y2
buying_investments = cumulative_investment_y2
buying_cash_spent = CLOSING_COSTS + net_costs_y1 + net_costs_y2
buying_net_worth = buying_home_equity + buying_investments - buying_cash_spent

print(f"  Home Value: ${property_value_y2:,.0f}")
print(f"  Mortgage Balance: -${balance_y2:,.0f}")
print(f"  Home Equity: ${buying_home_equity:,.0f}")
print(f"  Investments: ${buying_investments:,.0f}")
print(f"  Total Net Worth: ${buying_net_worth:,.0f}")

print("\n" + "="*80)
print("END OF ANALYSIS")
print("="*80)
