#!/usr/bin/env python3
"""
Complete Rent vs Buy Analysis - All Scenarios with Corrected Math
- 3% down with PMI
- 20% down (no PMI)
- Renting
All use monthly compounding for investment returns
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
    """Calculate interest and principal for a given year with monthly compounding"""
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
    """
    Calculate investment growth with monthly contributions using proper compounding
    Returns: (ending_balance, total_contributions, total_returns)
    """
    monthly_rate = INVESTMENT_RETURN / 12
    balance = starting_balance
    total_contributions = 0

    for month in range(months):
        # Compound existing balance
        balance = balance * (1 + monthly_rate)
        # Add monthly contribution
        balance += monthly_contribution
        total_contributions += monthly_contribution

    # Starting balance also grew
    total_value = balance
    starting_growth = starting_balance * ((1 + monthly_rate)**months - 1)
    contribution_returns = balance - starting_balance * (1 + monthly_rate)**months - total_contributions
    total_returns = total_value - starting_balance - total_contributions

    return total_value, total_contributions, total_returns

def calculate_tax_benefit(mortgage_interest, property_tax, loan_amount):
    """Calculate tax savings from itemizing"""
    # Cap mortgage interest deduction at $750K of debt
    if loan_amount > MORTGAGE_INTEREST_CAP:
        deductible_interest = mortgage_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
    else:
        deductible_interest = mortgage_interest

    # SALT deduction (property tax only, capped at $10K)
    salt_deduction = min(property_tax, SALT_CAP)

    # Total itemized deductions
    itemized = deductible_interest + salt_deduction

    # Compare to standard deduction
    excess = max(0, itemized - STANDARD_DEDUCTION)

    # Tax savings
    tax_savings = excess * TAX_RATE

    return tax_savings, deductible_interest, salt_deduction, itemized, excess

print("="*80)
print("COMPLETE RENT VS BUY ANALYSIS - ALL THREE SCENARIOS")
print("="*80)
print(f"\nParameters:")
print(f"  Property Price: ${PROPERTY_PRICE:,}")
print(f"  Starting Capital: ${STARTING_CAPITAL:,}")
print(f"  Home Appreciation: {HOME_APPRECIATION*100}%")
print(f"  Investment Return: {INVESTMENT_RETURN*100}% (monthly compounding)")
print(f"  Monthly Rent: ${MONTHLY_RENT:,}")
print()

# ============================================================================
# SCENARIO 1: 3% DOWN WITH PMI
# ============================================================================
print("="*80)
print("SCENARIO 1: 3% DOWN WITH PMI")
print("="*80)

down_3pct = PROPERTY_PRICE * 0.03
loan_3pct = PROPERTY_PRICE - down_3pct
upfront_3pct = down_3pct + CLOSING_COSTS
remaining_3pct = STARTING_CAPITAL - upfront_3pct

monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)
monthly_pmi_3pct = (PROPERTY_PRICE * PMI_RATE) / 12
monthly_tax_ins_3pct = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12

print(f"\nUPFRONT:")
print(f"  Down Payment (3%): ${down_3pct:,.0f}")
print(f"  Closing Costs: ${CLOSING_COSTS:,}")
print(f"  Total Upfront: ${upfront_3pct:,.0f}")
print(f"  Remaining to Invest: ${remaining_3pct:,.0f}")
print(f"  Loan Amount: ${loan_3pct:,.0f}")

print(f"\nMONTHLY COSTS:")
print(f"  Mortgage P&I: ${monthly_payment_3pct:,.2f}")
print(f"  PMI: ${monthly_pmi_3pct:,.2f}")
print(f"  Property Tax + Insurance: ${monthly_tax_ins_3pct:,.2f}")
print(f"  TOTAL MONTHLY: ${monthly_payment_3pct + monthly_pmi_3pct + monthly_tax_ins_3pct:,.2f}")

# YEAR 1 - 3% DOWN
print(f"\n{'='*80}")
print("YEAR 1 - 3% DOWN")
print('='*80)

property_value_y1 = PROPERTY_PRICE * (1 + HOME_APPRECIATION)
appreciation_y1 = property_value_y1 - PROPERTY_PRICE

interest_y1_3, principal_y1_3, balance_y1_3 = calculate_year_mortgage_breakdown(
    loan_3pct, monthly_payment_3pct)

# Investment growth (monthly compounding)
inv_eoy_y1_3, inv_contrib_y1_3, inv_returns_y1_3 = calculate_investment_growth_with_contributions(
    remaining_3pct, 0, 12)  # No additional monthly contributions

# Annual costs
property_tax_y1 = PROPERTY_PRICE * PROPERTY_TAX_RATE
pmi_y1_3 = PROPERTY_PRICE * PMI_RATE
total_costs_y1_3 = (monthly_payment_3pct * 12) + property_tax_y1 + HOME_INSURANCE_ANNUAL + pmi_y1_3

# Tax benefit
tax_savings_y1_3, deduct_int_3, salt_3, itemized_3, excess_3 = calculate_tax_benefit(
    interest_y1_3, property_tax_y1, loan_3pct)

net_costs_y1_3 = total_costs_y1_3 - tax_savings_y1_3

print(f"\n1. HOME APPRECIATION:")
print(f"   Property: ${PROPERTY_PRICE:,} → ${property_value_y1:,.0f}")
print(f"   Appreciation: +${appreciation_y1:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid: +${principal_y1_3:,.0f}")
print(f"   Mortgage: ${loan_3pct:,} → ${balance_y1_3:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Starting Balance: ${remaining_3pct:,.0f}")
print(f"   Ending Balance: ${inv_eoy_y1_3:,.0f}")
print(f"   Investment Returns (7% compounded): +${inv_returns_y1_3:,.0f}")

print(f"\n4. COSTS:")
print(f"   Mortgage P&I: ${monthly_payment_3pct * 12:,.0f}")
print(f"   Property Tax: ${property_tax_y1:,.0f}")
print(f"   Insurance: ${HOME_INSURANCE_ANNUAL:,}")
print(f"   PMI: ${pmi_y1_3:,.0f}")
print(f"   Total Before Tax: ${total_costs_y1_3:,.0f}")
print(f"\n   Tax Savings:")
print(f"     Mortgage Interest: ${interest_y1_3:,.0f}")
print(f"     Deductible (capped): ${deduct_int_3:,.0f}")
print(f"     SALT: ${salt_3:,.0f}")
print(f"     Itemized: ${itemized_3:,.0f} vs Standard: ${STANDARD_DEDUCTION:,}")
print(f"     Tax Benefit: ${tax_savings_y1_3:,.0f}")
print(f"   Net Costs (after tax): ${net_costs_y1_3:,.0f}")

print(f"\n5. NET POSITION YEAR 1:")
print(f"   Appreciation: +${appreciation_y1:,.0f}")
print(f"   Equity: +${principal_y1_3:,.0f}")
print(f"   Investment Returns: +${inv_returns_y1_3:,.0f}")
print(f"   Net Costs: -${net_costs_y1_3:,.0f}")
print(f"   Closing Costs: -${CLOSING_COSTS:,}")
print(f"   {'─'*60}")
net_y1_3 = appreciation_y1 + principal_y1_3 + inv_returns_y1_3 - net_costs_y1_3 - CLOSING_COSTS
print(f"   TOTAL NET YEAR 1: ${net_y1_3:,.0f}")

# YEAR 2 - 3% DOWN
print(f"\n{'='*80}")
print("YEAR 2 - 3% DOWN")
print('='*80)

property_value_y2 = property_value_y1 * (1 + HOME_APPRECIATION)
appreciation_y2 = property_value_y2 - property_value_y1

interest_y2_3, principal_y2_3, balance_y2_3 = calculate_year_mortgage_breakdown(
    balance_y1_3, monthly_payment_3pct)

# Check if PMI can be removed (need 20% equity)
equity_pct_y2_3 = (property_value_y2 - balance_y2_3) / PROPERTY_PRICE
pmi_y2_3 = 0 if equity_pct_y2_3 >= 0.20 else PROPERTY_PRICE * PMI_RATE

inv_eoy_y2_3, inv_contrib_y2_3, inv_returns_y2_3 = calculate_investment_growth_with_contributions(
    inv_eoy_y1_3, 0, 12)

property_tax_y2 = property_tax_y1 * 1.02
home_ins_y2 = HOME_INSURANCE_ANNUAL * 1.03
total_costs_y2_3 = (monthly_payment_3pct * 12) + property_tax_y2 + home_ins_y2 + pmi_y2_3

tax_savings_y2_3, _, _, _, _ = calculate_tax_benefit(interest_y2_3, property_tax_y2, balance_y1_3)
net_costs_y2_3 = total_costs_y2_3 - tax_savings_y2_3

print(f"\n1. HOME APPRECIATION:")
print(f"   Property: ${property_value_y1:,.0f} → ${property_value_y2:,.0f}")
print(f"   Appreciation Year 2: +${appreciation_y2:,.0f}")
print(f"   Cumulative: ${property_value_y2 - PROPERTY_PRICE:,.0f}")

print(f"\n2. HOME EQUITY:")
print(f"   Principal Year 2: +${principal_y2_3:,.0f}")
print(f"   Cumulative Principal: ${principal_y1_3 + principal_y2_3:,.0f}")
print(f"   Equity %: {equity_pct_y2_3*100:.1f}%")
print(f"   PMI Status: {'REMOVED!' if pmi_y2_3 == 0 else 'Still paying'}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Balance: ${inv_eoy_y1_3:,.0f} → ${inv_eoy_y2_3:,.0f}")
print(f"   Returns Year 2: +${inv_returns_y2_3:,.0f}")

print(f"\n4. NET POSITION YEAR 2:")
print(f"   Appreciation: +${appreciation_y2:,.0f}")
print(f"   Equity: +${principal_y2_3:,.0f}")
print(f"   Investment Returns: +${inv_returns_y2_3:,.0f}")
print(f"   Net Costs: -${net_costs_y2_3:,.0f}")
print(f"   {'─'*60}")
net_y2_3 = appreciation_y2 + principal_y2_3 + inv_returns_y2_3 - net_costs_y2_3
print(f"   TOTAL NET YEAR 2: ${net_y2_3:,.0f}")

# ============================================================================
# SCENARIO 2: 20% DOWN
# ============================================================================
print(f"\n\n{'='*80}")
print("SCENARIO 2: 20% DOWN (NO PMI)")
print("="*80)

down_20pct = PROPERTY_PRICE * 0.20
loan_20pct = PROPERTY_PRICE - down_20pct
upfront_20pct = down_20pct + CLOSING_COSTS
remaining_20pct = STARTING_CAPITAL - upfront_20pct

monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)
monthly_tax_ins_20pct = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12

print(f"\nUPFRONT:")
print(f"  Down Payment (20%): ${down_20pct:,.0f}")
print(f"  Closing Costs: ${CLOSING_COSTS:,}")
print(f"  Total Upfront: ${upfront_20pct:,.0f}")
print(f"  Remaining to Invest: ${remaining_20pct:,.0f}")
print(f"  Loan Amount: ${loan_20pct:,.0f}")

print(f"\nMONTHLY COSTS:")
print(f"  Mortgage P&I: ${monthly_payment_20pct:,.2f}")
print(f"  PMI: $0 (20% down!)")
print(f"  Property Tax + Insurance: ${monthly_tax_ins_20pct:,.2f}")
print(f"  TOTAL MONTHLY: ${monthly_payment_20pct + monthly_tax_ins_20pct:,.2f}")

# YEAR 1 - 20% DOWN
print(f"\n{'='*80}")
print("YEAR 1 - 20% DOWN")
print('='*80)

interest_y1_20, principal_y1_20, balance_y1_20 = calculate_year_mortgage_breakdown(
    loan_20pct, monthly_payment_20pct)

# No starting investment balance (all went to down payment)
inv_eoy_y1_20, inv_contrib_y1_20, inv_returns_y1_20 = calculate_investment_growth_with_contributions(
    0, 0, 12)  # Starting from $0

total_costs_y1_20 = (monthly_payment_20pct * 12) + property_tax_y1 + HOME_INSURANCE_ANNUAL

tax_savings_y1_20, deduct_int_20, salt_20, itemized_20, excess_20 = calculate_tax_benefit(
    interest_y1_20, property_tax_y1, loan_20pct)

net_costs_y1_20 = total_costs_y1_20 - tax_savings_y1_20

print(f"\n1. HOME APPRECIATION:")
print(f"   Appreciation: +${appreciation_y1:,.0f}")

print(f"\n2. HOME EQUITY (Principal Paid):")
print(f"   Principal Paid: +${principal_y1_20:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Starting Balance: $0 (all capital spent on down payment)")
print(f"   Investment Returns: +${inv_returns_y1_20:,.0f}")

print(f"\n4. COSTS:")
print(f"   Total Before Tax: ${total_costs_y1_20:,.0f}")
print(f"   Tax Benefit: ${tax_savings_y1_20:,.0f}")
print(f"   Net Costs: ${net_costs_y1_20:,.0f}")

print(f"\n5. NET POSITION YEAR 1:")
print(f"   Appreciation: +${appreciation_y1:,.0f}")
print(f"   Equity: +${principal_y1_20:,.0f}")
print(f"   Investment Returns: +${inv_returns_y1_20:,.0f}")
print(f"   Net Costs: -${net_costs_y1_20:,.0f}")
print(f"   Closing Costs: -${CLOSING_COSTS:,}")
print(f"   {'─'*60}")
net_y1_20 = appreciation_y1 + principal_y1_20 + inv_returns_y1_20 - net_costs_y1_20 - CLOSING_COSTS
print(f"   TOTAL NET YEAR 1: ${net_y1_20:,.0f}")

# YEAR 2 - 20% DOWN
print(f"\n{'='*80}")
print("YEAR 2 - 20% DOWN")
print('='*80)

interest_y2_20, principal_y2_20, balance_y2_20 = calculate_year_mortgage_breakdown(
    balance_y1_20, monthly_payment_20pct)

inv_eoy_y2_20, inv_contrib_y2_20, inv_returns_y2_20 = calculate_investment_growth_with_contributions(
    inv_eoy_y1_20, 0, 12)

total_costs_y2_20 = (monthly_payment_20pct * 12) + property_tax_y2 + home_ins_y2
tax_savings_y2_20, _, _, _, _ = calculate_tax_benefit(interest_y2_20, property_tax_y2, balance_y1_20)
net_costs_y2_20 = total_costs_y2_20 - tax_savings_y2_20

print(f"\n1. HOME APPRECIATION:")
print(f"   Appreciation Year 2: +${appreciation_y2:,.0f}")

print(f"\n2. HOME EQUITY:")
print(f"   Principal Year 2: +${principal_y2_20:,.0f}")
print(f"   Total Equity: ${property_value_y2 - balance_y2_20:,.0f}")

print(f"\n3. INVESTMENT RETURNS:")
print(f"   Returns Year 2: +${inv_returns_y2_20:,.0f}")

print(f"\n4. NET POSITION YEAR 2:")
print(f"   Appreciation: +${appreciation_y2:,.0f}")
print(f"   Equity: +${principal_y2_20:,.0f}")
print(f"   Investment Returns: +${inv_returns_y2_20:,.0f}")
print(f"   Net Costs: -${net_costs_y2_20:,.0f}")
print(f"   {'─'*60}")
net_y2_20 = appreciation_y2 + principal_y2_20 + inv_returns_y2_20 - net_costs_y2_20
print(f"   TOTAL NET YEAR 2: ${net_y2_20:,.0f}")

# ============================================================================
# SCENARIO 3: RENTING
# ============================================================================
print(f"\n\n{'='*80}")
print("SCENARIO 3: RENTING")
print("="*80)

print(f"\nSTARTING:")
print(f"  Capital to Invest: ${STARTING_CAPITAL:,}")
print(f"  Monthly Rent: ${MONTHLY_RENT:,}")

# YEAR 1 - RENTING
print(f"\n{'='*80}")
print("YEAR 1 - RENTING")
print('='*80)

inv_eoy_y1_rent, _, inv_returns_y1_rent = calculate_investment_growth_with_contributions(
    STARTING_CAPITAL, 0, 12)

rent_y1 = MONTHLY_RENT * 12

print(f"\n1. INVESTMENT RETURNS:")
print(f"   Starting: ${STARTING_CAPITAL:,}")
print(f"   Ending: ${inv_eoy_y1_rent:,.0f}")
print(f"   Returns (7% compounded): +${inv_returns_y1_rent:,.0f}")

print(f"\n2. RENT PAID:")
print(f"   Annual Rent: -${rent_y1:,.0f}")

print(f"\n3. NET POSITION YEAR 1:")
print(f"   Investment Returns: +${inv_returns_y1_rent:,.0f}")
print(f"   Rent: -${rent_y1:,.0f}")
print(f"   {'─'*60}")
net_y1_rent = inv_returns_y1_rent - rent_y1
print(f"   TOTAL NET YEAR 1: ${net_y1_rent:,.0f}")

# YEAR 2 - RENTING
print(f"\n{'='*80}")
print("YEAR 2 - RENTING")
print('='*80)

inv_eoy_y2_rent, _, inv_returns_y2_rent = calculate_investment_growth_with_contributions(
    inv_eoy_y1_rent, 0, 12)

rent_y2 = rent_y1 * (1 + RENT_GROWTH)

print(f"\n1. INVESTMENT RETURNS:")
print(f"   Starting: ${inv_eoy_y1_rent:,.0f}")
print(f"   Ending: ${inv_eoy_y2_rent:,.0f}")
print(f"   Returns Year 2: +${inv_returns_y2_rent:,.0f}")

print(f"\n2. RENT PAID:")
print(f"   Annual Rent (up 3%): -${rent_y2:,.0f}")

print(f"\n3. NET POSITION YEAR 2:")
print(f"   Investment Returns: +${inv_returns_y2_rent:,.0f}")
print(f"   Rent: -${rent_y2:,.0f}")
print(f"   {'─'*60}")
net_y2_rent = inv_returns_y2_rent - rent_y2
print(f"   TOTAL NET YEAR 2: ${net_y2_rent:,.0f}")

# ============================================================================
# FINAL COMPARISON
# ============================================================================
print(f"\n\n{'='*80}")
print("FINAL COMPARISON - ALL THREE SCENARIOS")
print("="*80)

print(f"\nYEAR 1 NET POSITION:")
print(f"  3% Down + PMI:  ${net_y1_3:>10,.0f}")
print(f"  20% Down:       ${net_y1_20:>10,.0f}")
print(f"  Renting:        ${net_y1_rent:>10,.0f}")
winner_y1 = max(net_y1_3, net_y1_20, net_y1_rent)
if winner_y1 == net_y1_3:
    print(f"  Winner: 3% Down (by ${net_y1_3 - max(net_y1_20, net_y1_rent):,.0f})")
elif winner_y1 == net_y1_20:
    print(f"  Winner: 20% Down (by ${net_y1_20 - max(net_y1_3, net_y1_rent):,.0f})")
else:
    print(f"  Winner: Renting (by ${net_y1_rent - max(net_y1_3, net_y1_20):,.0f})")

print(f"\nYEAR 2 NET POSITION:")
print(f"  3% Down + PMI:  ${net_y2_3:>10,.0f}")
print(f"  20% Down:       ${net_y2_20:>10,.0f}")
print(f"  Renting:        ${net_y2_rent:>10,.0f}")
winner_y2 = max(net_y2_3, net_y2_20, net_y2_rent)
if winner_y2 == net_y2_3:
    print(f"  Winner: 3% Down (by ${net_y2_3 - max(net_y2_20, net_y2_rent):,.0f})")
elif winner_y2 == net_y2_20:
    print(f"  Winner: 20% Down (by ${net_y2_20 - max(net_y2_3, net_y2_rent):,.0f})")
else:
    print(f"  Winner: Renting (by ${net_y2_rent - max(net_y2_3, net_y2_20):,.0f})")

print(f"\nCUMULATIVE 2-YEAR:")
cumulative_3 = net_y1_3 + net_y2_3
cumulative_20 = net_y1_20 + net_y2_20
cumulative_rent = net_y1_rent + net_y2_rent
print(f"  3% Down + PMI:  ${cumulative_3:>10,.0f}")
print(f"  20% Down:       ${cumulative_20:>10,.0f}")
print(f"  Renting:        ${cumulative_rent:>10,.0f}")
winner_cum = max(cumulative_3, cumulative_20, cumulative_rent)
if winner_cum == cumulative_3:
    print(f"  Winner: 3% Down (by ${cumulative_3 - max(cumulative_20, cumulative_rent):,.0f})")
elif winner_cum == cumulative_20:
    print(f"  Winner: 20% Down (by ${cumulative_20 - max(cumulative_3, cumulative_rent):,.0f})")
else:
    print(f"  Winner: Renting (by ${cumulative_rent - max(cumulative_3, cumulative_20):,.0f})")

print(f"\n\nTOTAL NET WORTH AFTER 2 YEARS:")
print(f"\n3% Down:")
equity_3 = property_value_y2 - balance_y2_3
print(f"  Home Equity:    ${equity_3:>10,.0f}")
print(f"  Investments:    ${inv_eoy_y2_3:>10,.0f}")
print(f"  TOTAL:          ${equity_3 + inv_eoy_y2_3:>10,.0f}")

print(f"\n20% Down:")
equity_20 = property_value_y2 - balance_y2_20
print(f"  Home Equity:    ${equity_20:>10,.0f}")
print(f"  Investments:    ${inv_eoy_y2_20:>10,.0f}")
print(f"  TOTAL:          ${equity_20 + inv_eoy_y2_20:>10,.0f}")

print(f"\nRenting:")
print(f"  Home Equity:    $         0")
print(f"  Investments:    ${inv_eoy_y2_rent:>10,.0f}")
print(f"  TOTAL:          ${inv_eoy_y2_rent:>10,.0f}")

print("\n" + "="*80)
