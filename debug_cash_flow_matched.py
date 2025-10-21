#!/usr/bin/env python3
"""
Debug Rent vs Buy Projections - Cash Flow Matched
Constraint: Monthly income is same for all scenarios (matched to 3% down payment)
- 3% down person pays highest monthly cost (mortgage + PMI + taxes + insurance)
- 20% down person pays less monthly, invests the difference
- Renter pays rent, invests the difference vs 3% down cost
"""

# Constants
PROPERTY_PRICE = 1_900_000
MONTHLY_RENT = 5_800
STARTING_CAPITAL = 410_000
MORTGAGE_RATE = 0.06
PROPERTY_TAX_RATE = 0.012
HOME_INSURANCE_ANNUAL = 3_000
CLOSING_COSTS = 30_000
RENT_GROWTH = 0.03
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
TAX_RATE = 0.413  # 32% federal + 9.3% CA
STANDARD_DEDUCTION = 31_500  # Married
MORTGAGE_INTEREST_CAP = 750_000
SALT_CAP = 10_000
PMI_RATE = 0.01  # 1% of purchase price annually

def calculate_monthly_mortgage_payment(principal, annual_rate, years=30):
    """Calculate monthly P&I payment"""
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment

def calculate_year_mortgage_breakdown(principal_remaining, monthly_payment):
    """Calculate interest and principal for a given year"""
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

print("="*80)
print("RENT VS BUY - CASH FLOW MATCHED ANALYSIS")
print("="*80)
print(f"\nCONSTRAINT: Monthly income is same as 3% down scenario")
print(f"All scenarios invest surplus cash flow vs. 3% down baseline")
print()

# First, calculate 3% down scenario to establish baseline monthly cost
print("="*80)
print("STEP 1: ESTABLISH BASELINE (3% DOWN SCENARIO)")
print("="*80)

down_3pct = PROPERTY_PRICE * 0.03
loan_3pct = PROPERTY_PRICE - down_3pct
monthly_pmi = (PROPERTY_PRICE * PMI_RATE) / 12
monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)
monthly_tax_insurance_3pct = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12
monthly_total_3pct = monthly_payment_3pct + monthly_pmi + monthly_tax_insurance_3pct
annual_total_3pct = monthly_total_3pct * 12

print(f"\n3% DOWN SCENARIO:")
print(f"  Down Payment: ${down_3pct:,.0f}")
print(f"  Loan Amount: ${loan_3pct:,.0f}")
print(f"  Monthly P&I: ${monthly_payment_3pct:,.2f}")
print(f"  Monthly PMI: ${monthly_pmi:,.2f}")
print(f"  Monthly Tax+Insurance: ${monthly_tax_insurance_3pct:,.2f}")
print(f"  TOTAL MONTHLY COST: ${monthly_total_3pct:,.2f}")
print(f"  TOTAL ANNUAL COST: ${annual_total_3pct:,.2f}")

BASELINE_MONTHLY = monthly_total_3pct

# Now calculate 20% down scenario
print("\n" + "="*80)
print("STEP 2: 20% DOWN SCENARIO")
print("="*80)

down_20pct = PROPERTY_PRICE * 0.20
loan_20pct = PROPERTY_PRICE - down_20pct
monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)
monthly_tax_insurance_20pct = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12
monthly_total_20pct = monthly_payment_20pct + monthly_tax_insurance_20pct  # No PMI!
annual_total_20pct = monthly_total_20pct * 12

monthly_savings_20pct = BASELINE_MONTHLY - monthly_total_20pct
annual_savings_20pct = monthly_savings_20pct * 12

print(f"\n20% DOWN SCENARIO:")
print(f"  Down Payment: ${down_20pct:,.0f}")
print(f"  Loan Amount: ${loan_20pct:,.0f}")
print(f"  Monthly P&I: ${monthly_payment_20pct:,.2f}")
print(f"  Monthly PMI: $0 (no PMI with 20% down!)")
print(f"  Monthly Tax+Insurance: ${monthly_tax_insurance_20pct:,.2f}")
print(f"  TOTAL MONTHLY COST: ${monthly_total_20pct:,.2f}")
print(f"  TOTAL ANNUAL COST: ${annual_total_20pct:,.2f}")
print(f"\n  MONTHLY SAVINGS vs 3% down: ${monthly_savings_20pct:,.2f}")
print(f"  ANNUAL SAVINGS to invest: ${annual_savings_20pct:,.2f}")

# Renting scenario
monthly_savings_rent = BASELINE_MONTHLY - MONTHLY_RENT
annual_savings_rent = monthly_savings_rent * 12

print("\n" + "="*80)
print("STEP 3: RENTING SCENARIO")
print("="*80)
print(f"  Monthly Rent: ${MONTHLY_RENT:,.2f}")
print(f"  Baseline Monthly (3% down): ${BASELINE_MONTHLY:,.2f}")
print(f"  MONTHLY SAVINGS vs 3% down: ${monthly_savings_rent:,.2f}")
print(f"  ANNUAL SAVINGS to invest: ${annual_savings_rent:,.2f}")

# YEAR 1 - 20% DOWN
print("\n" + "="*80)
print("YEAR 1 - 20% DOWN (with monthly savings invested)")
print("="*80)

# Starting investment: $410K - down payment - closing costs
upfront_20pct = down_20pct + CLOSING_COSTS
starting_investment_20pct = STARTING_CAPITAL - upfront_20pct

print(f"\nSTARTING POSITION:")
print(f"  Starting Capital: ${STARTING_CAPITAL:,}")
print(f"  Down Payment: ${down_20pct:,.0f}")
print(f"  Closing Costs: ${CLOSING_COSTS:,}")
print(f"  Remaining to Invest: ${starting_investment_20pct:,.0f}")

property_value_y1 = PROPERTY_PRICE * (1 + HOME_APPRECIATION)
appreciation_y1 = property_value_y1 - PROPERTY_PRICE

interest_y1_20, principal_y1_20, balance_y1_20 = calculate_year_mortgage_breakdown(
    loan_20pct, monthly_payment_20pct)

# Tax calculation for 20% down
property_tax_y1 = PROPERTY_PRICE * PROPERTY_TAX_RATE
deductible_interest_20 = min(interest_y1_20, (MORTGAGE_INTEREST_CAP / loan_20pct) * interest_y1_20)
salt_deduction_20 = min(property_tax_y1, SALT_CAP)
itemized_20 = deductible_interest_20 + salt_deduction_20
excess_20 = max(0, itemized_20 - STANDARD_DEDUCTION)
tax_savings_y1_20 = excess_20 * TAX_RATE

net_costs_y1_20 = annual_total_20pct - tax_savings_y1_20

# Investment returns: starting balance + monthly contributions
# Simplified: invest lump sum at start + annual savings at end
# More accurate: compound monthly, but let's do simplified first
investment_return_y1_base = starting_investment_20pct * INVESTMENT_RETURN
investment_return_y1_flow = annual_savings_20pct * (INVESTMENT_RETURN / 2)  # Half year average
total_investment_return_y1 = investment_return_y1_base + investment_return_y1_flow

print(f"\n1. HOME APPRECIATION:")
print(f"   Property Value Start: ${PROPERTY_PRICE:,}")
print(f"   Property Value End: ${property_value_y1:,.0f}")
print(f"   Appreciation (3%): ${appreciation_y1:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid Year 1: ${principal_y1_20:,.0f}")
print(f"   Mortgage Balance: ${loan_20pct:,} → ${balance_y1_20:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Starting Investment Balance: ${starting_investment_20pct:,.0f}")
print(f"   Return on Starting Balance (7%): ${investment_return_y1_base:,.0f}")
print(f"   Annual Cash Flow Savings: ${annual_savings_20pct:,.0f}")
print(f"   Return on Flow (~3.5% half-year): ${investment_return_y1_flow:,.0f}")
print(f"   Total Investment Returns Year 1: ${total_investment_return_y1:,.0f}")

print(f"\n4. COSTS (after tax):")
print(f"   Annual Costs Before Tax: ${annual_total_20pct:,.0f}")
print(f"   Tax Savings: ${tax_savings_y1_20:,.0f}")
print(f"   Net Costs: ${net_costs_y1_20:,.0f}")

print(f"\n5. NET POSITION YEAR 1:")
print(f"   Home Appreciation: +${appreciation_y1:,.0f}")
print(f"   Home Equity (principal): +${principal_y1_20:,.0f}")
print(f"   Investment Returns: +${total_investment_return_y1:,.0f}")
print(f"   Net Costs (after tax): -${net_costs_y1_20:,.0f}")
print(f"   Closing Costs (one-time): -${CLOSING_COSTS:,}")
print(f"   -------------------------------------------------------")
net_y1_20 = appreciation_y1 + principal_y1_20 + total_investment_return_y1 - net_costs_y1_20 - CLOSING_COSTS
print(f"   TOTAL NET YEAR 1: ${net_y1_20:,.0f}")

# Investment balance at end of year 1
investment_eoy_y1_20 = starting_investment_20pct + investment_return_y1_base + \
                       annual_savings_20pct + investment_return_y1_flow

print(f"\n6. INVESTMENT BALANCE END OF YEAR 1:")
print(f"   Starting: ${starting_investment_20pct:,.0f}")
print(f"   Returns: +${total_investment_return_y1:,.0f}")
print(f"   Contributions: +${annual_savings_20pct:,.0f}")
print(f"   Total: ${investment_eoy_y1_20:,.0f}")

# YEAR 2 - 20% DOWN
print("\n" + "="*80)
print("YEAR 2 - 20% DOWN (with monthly savings invested)")
print("="*80)

property_value_y2 = property_value_y1 * (1 + HOME_APPRECIATION)
appreciation_y2 = property_value_y2 - property_value_y1

interest_y2_20, principal_y2_20, balance_y2_20 = calculate_year_mortgage_breakdown(
    balance_y1_20, monthly_payment_20pct)

# Tax calculation year 2
property_tax_y2 = property_tax_y1 * 1.02
home_insurance_y2 = HOME_INSURANCE_ANNUAL * 1.03
annual_total_20pct_y2 = (monthly_payment_20pct * 12) + property_tax_y2 + home_insurance_y2

deductible_interest_20_y2 = min(interest_y2_20, (MORTGAGE_INTEREST_CAP / balance_y1_20) * interest_y2_20)
salt_deduction_20_y2 = min(property_tax_y2, SALT_CAP)
itemized_20_y2 = deductible_interest_20_y2 + salt_deduction_20_y2
excess_20_y2 = max(0, itemized_20_y2 - STANDARD_DEDUCTION)
tax_savings_y2_20 = excess_20_y2 * TAX_RATE

net_costs_y2_20 = annual_total_20pct_y2 - tax_savings_y2_20

# Investment returns year 2
investment_return_y2_base = investment_eoy_y1_20 * INVESTMENT_RETURN
investment_return_y2_flow = annual_savings_20pct * (INVESTMENT_RETURN / 2)
total_investment_return_y2 = investment_return_y2_base + investment_return_y2_flow

print(f"\n1. HOME APPRECIATION:")
print(f"   Property Value Start: ${property_value_y1:,.0f}")
print(f"   Property Value End: ${property_value_y2:,.0f}")
print(f"   Appreciation Year 2: ${appreciation_y2:,.0f}")
print(f"   Cumulative Appreciation: ${property_value_y2 - PROPERTY_PRICE:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid Year 2: ${principal_y2_20:,.0f}")
print(f"   Cumulative Principal: ${principal_y1_20 + principal_y2_20:,.0f}")
print(f"   Total Home Equity: ${property_value_y2 - balance_y2_20:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Starting Investment Balance: ${investment_eoy_y1_20:,.0f}")
print(f"   Return on Starting Balance (7%): ${investment_return_y2_base:,.0f}")
print(f"   Annual Cash Flow Savings: ${annual_savings_20pct:,.0f}")
print(f"   Return on Flow (~3.5%): ${investment_return_y2_flow:,.0f}")
print(f"   Total Investment Returns Year 2: ${total_investment_return_y2:,.0f}")

print(f"\n4. COSTS (after tax):")
print(f"   Annual Costs Before Tax: ${annual_total_20pct_y2:,.0f}")
print(f"   Tax Savings: ${tax_savings_y2_20:,.0f}")
print(f"   Net Costs: ${net_costs_y2_20:,.0f}")

print(f"\n5. NET POSITION YEAR 2:")
print(f"   Home Appreciation: +${appreciation_y2:,.0f}")
print(f"   Home Equity (principal): +${principal_y2_20:,.0f}")
print(f"   Investment Returns: +${total_investment_return_y2:,.0f}")
print(f"   Net Costs (after tax): -${net_costs_y2_20:,.0f}")
print(f"   -------------------------------------------------------")
net_y2_20 = appreciation_y2 + principal_y2_20 + total_investment_return_y2 - net_costs_y2_20
print(f"   TOTAL NET YEAR 2: ${net_y2_20:,.0f}")

investment_eoy_y2_20 = investment_eoy_y1_20 + investment_return_y2_base + \
                       annual_savings_20pct + investment_return_y2_flow

print(f"\n6. INVESTMENT BALANCE END OF YEAR 2:")
print(f"   Total: ${investment_eoy_y2_20:,.0f}")

# RENTING YEARS 1 & 2
print("\n" + "="*80)
print("YEAR 1 - RENTING (with monthly savings invested)")
print("="*80)

starting_investment_rent = STARTING_CAPITAL
investment_return_y1_rent_base = starting_investment_rent * INVESTMENT_RETURN
investment_return_y1_rent_flow = annual_savings_rent * (INVESTMENT_RETURN / 2)
total_investment_return_y1_rent = investment_return_y1_rent_base + investment_return_y1_rent_flow

rent_y1 = MONTHLY_RENT * 12

print(f"\nSTARTING POSITION:")
print(f"  Starting Capital: ${starting_investment_rent:,}")
print(f"  No upfront costs")

print(f"\nINVESTMENT RETURNS:")
print(f"  Return on Starting Balance (7%): ${investment_return_y1_rent_base:,.0f}")
print(f"  Annual Cash Flow Savings: ${annual_savings_rent:,.0f}")
print(f"  Return on Flow (~3.5%): ${investment_return_y1_rent_flow:,.0f}")
print(f"  Total Investment Returns: ${total_investment_return_y1_rent:,.0f}")

print(f"\nCOSTS:")
print(f"  Annual Rent: ${rent_y1:,.0f}")

print(f"\nNET POSITION YEAR 1:")
print(f"  Investment Returns: +${total_investment_return_y1_rent:,.0f}")
print(f"  Rent Paid: -${rent_y1:,.0f}")
print(f"  -------------------------------------------------------")
net_y1_rent = total_investment_return_y1_rent - rent_y1
print(f"  TOTAL NET YEAR 1: ${net_y1_rent:,.0f}")

investment_eoy_y1_rent = starting_investment_rent + investment_return_y1_rent_base + \
                         annual_savings_rent + investment_return_y1_rent_flow

print(f"\nINVESTMENT BALANCE END OF YEAR 1: ${investment_eoy_y1_rent:,.0f}")

print("\n" + "="*80)
print("YEAR 2 - RENTING (with monthly savings invested)")
print("="*80)

investment_return_y2_rent_base = investment_eoy_y1_rent * INVESTMENT_RETURN
investment_return_y2_rent_flow = annual_savings_rent * (INVESTMENT_RETURN / 2)
total_investment_return_y2_rent = investment_return_y2_rent_base + investment_return_y2_rent_flow

rent_y2 = rent_y1 * (1 + RENT_GROWTH)

print(f"\nINVESTMENT RETURNS:")
print(f"  Starting Balance: ${investment_eoy_y1_rent:,.0f}")
print(f"  Return on Starting Balance (7%): ${investment_return_y2_rent_base:,.0f}")
print(f"  Annual Cash Flow Savings: ${annual_savings_rent:,.0f}")
print(f"  Return on Flow (~3.5%): ${investment_return_y2_rent_flow:,.0f}")
print(f"  Total Investment Returns: ${total_investment_return_y2_rent:,.0f}")

print(f"\nCOSTS:")
print(f"  Annual Rent: ${rent_y2:,.0f}")

print(f"\nNET POSITION YEAR 2:")
print(f"  Investment Returns: +${total_investment_return_y2_rent:,.0f}")
print(f"  Rent Paid: -${rent_y2:,.0f}")
print(f"  -------------------------------------------------------")
net_y2_rent = total_investment_return_y2_rent - rent_y2
print(f"  TOTAL NET YEAR 2: ${net_y2_rent:,.0f}")

investment_eoy_y2_rent = investment_eoy_y1_rent + investment_return_y2_rent_base + \
                         annual_savings_rent + investment_return_y2_rent_flow

print(f"\nINVESTMENT BALANCE END OF YEAR 2: ${investment_eoy_y2_rent:,.0f}")

# FINAL COMPARISON
print("\n" + "="*80)
print("FINAL COMPARISON")
print("="*80)

print(f"\nYEAR 1 NET POSITION:")
print(f"  Renting: ${net_y1_rent:,.0f}")
print(f"  20% Down: ${net_y1_20:,.0f}")
print(f"  Difference: ${net_y1_20 - net_y1_rent:,.0f} " +
      ("(Buying wins)" if net_y1_20 > net_y1_rent else "(Renting wins)"))

print(f"\nYEAR 2 NET POSITION:")
print(f"  Renting: ${net_y2_rent:,.0f}")
print(f"  20% Down: ${net_y2_20:,.0f}")
print(f"  Difference: ${net_y2_20 - net_y2_rent:,.0f} " +
      ("(Buying wins)" if net_y2_20 > net_y2_rent else "(Renting wins)"))

print(f"\nCUMULATIVE 2-YEAR:")
cumulative_rent = net_y1_rent + net_y2_rent
cumulative_buy = net_y1_20 + net_y2_20
print(f"  Renting: ${cumulative_rent:,.0f}")
print(f"  20% Down: ${cumulative_buy:,.0f}")
print(f"  Difference: ${cumulative_buy - cumulative_rent:,.0f} " +
      ("(Buying wins)" if cumulative_buy > cumulative_rent else "(Renting wins)"))

print(f"\nTOTAL NET WORTH AFTER 2 YEARS:")
print(f"\nRenting:")
print(f"  Investments: ${investment_eoy_y2_rent:,.0f}")
print(f"  Home Equity: $0")
print(f"  Total: ${investment_eoy_y2_rent:,.0f}")

print(f"\n20% Down Buying:")
home_equity_y2 = property_value_y2 - balance_y2_20
print(f"  Home Equity: ${home_equity_y2:,.0f}")
print(f"  Investments: ${investment_eoy_y2_20:,.0f}")
print(f"  Total: ${home_equity_y2 + investment_eoy_y2_20:,.0f}")

print(f"\nNET WORTH DIFFERENCE: ${(home_equity_y2 + investment_eoy_y2_20) - investment_eoy_y2_rent:,.0f}")

print("\n" + "="*80)
