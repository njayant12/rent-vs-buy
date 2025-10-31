#!/usr/bin/env python3
"""
Year 1 Detailed Check - 50 Year Analysis
Federal tax benefits only (CA tax cancels with standard deduction)
"""

import math

print("=" * 80)
print("YEAR 1 DETAILED CALCULATION - ALL CHECKS")
print("=" * 80)
print()

# ============================================================================
# INITIAL VALUES
# ============================================================================

HOME_PRICE = 1_900_000
JUBILEE_HOUSE_VALUE = HOME_PRICE * 0.40
JUBILEE_LAND_VALUE = HOME_PRICE * 0.60

# Loans
JUBILEE_LOAN = 746_234  # Includes upfront PMI
TRADITIONAL_LOAN = 1_520_000

# Interest rates
JUBILEE_RATE = 0.0625
TRADITIONAL_RATE = 0.0615

# Tax rates (FEDERAL ONLY)
FEDERAL_TAX_RATE = 0.32
STANDARD_DEDUCTION = 29_200

# Investment return
ANNUAL_RETURN = 0.07
MONTHLY_RETURN = ANNUAL_RETURN / 12

print("=" * 80)
print("CHECK 1: YEAR 1 MONTHLY COSTS")
print("=" * 80)
print()

# ============================================================================
# JUBILEE YEAR 1
# ============================================================================

print("JUBILEE:")
print("-" * 40)

# Fixed costs
jubilee_mortgage = 4_595  # From previous calculation
jubilee_pmi = 336
jubilee_land_lease = 6_650  # Fixed years 1-5
jubilee_property_tax = 1_868
jubilee_insurance = 125
jubilee_maintenance = 675

jubilee_pretax = (jubilee_mortgage + jubilee_pmi + jubilee_land_lease +
                 jubilee_property_tax + jubilee_insurance + jubilee_maintenance)

print(f"  Mortgage P&I:      ${jubilee_mortgage:>6,}")
print(f"  PMI:               ${jubilee_pmi:>6,}")
print(f"  Land lease:        ${jubilee_land_lease:>6,}")
print(f"  Property tax:      ${jubilee_property_tax:>6,}")
print(f"  Insurance:         ${jubilee_insurance:>6,}")
print(f"  Maintenance:       ${jubilee_maintenance:>6,}")
print(f"  PRE-TAX TOTAL:     ${jubilee_pretax:>6,}/month")
print()

# ============================================================================
# TRADITIONAL YEAR 1
# ============================================================================

print("TRADITIONAL 20% DOWN:")
print("-" * 40)

traditional_mortgage = 9_260
traditional_property_tax = 1_868
traditional_insurance = 125
traditional_maintenance = 675

traditional_pretax = (traditional_mortgage + traditional_property_tax +
                     traditional_insurance + traditional_maintenance)

print(f"  Mortgage P&I:      ${traditional_mortgage:>6,}")
print(f"  Property tax:      ${traditional_property_tax:>6,}")
print(f"  Insurance:         ${traditional_insurance:>6,}")
print(f"  Maintenance:       ${traditional_maintenance:>6,}")
print(f"  PRE-TAX TOTAL:     ${traditional_pretax:>6,}/month")
print()

# ============================================================================
# RENTING YEAR 1
# ============================================================================

print("RENTING:")
print("-" * 40)

renting_rent = 5_800
renting_insurance = 17
renting_total = renting_rent + renting_insurance

print(f"  Rent:              ${renting_rent:>6,}")
print(f"  Insurance:         ${renting_insurance:>6,}")
print(f"  TOTAL:             ${renting_total:>6,}/month")
print()

# ============================================================================
# CHECK 2: TAX BENEFIT CALCULATION (FEDERAL ONLY)
# ============================================================================

print("=" * 80)
print("CHECK 2: FEDERAL TAX BENEFITS (Year 1)")
print("=" * 80)
print()

print("JUBILEE TAX BENEFIT:")
print("-" * 40)

# Mortgage interest in Year 1 (approximately principal × rate)
jubilee_annual_interest = JUBILEE_LOAN * JUBILEE_RATE
print(f"  Year 1 mortgage interest: ${jubilee_annual_interest:>10,.0f}")

# Federal deductions
jubilee_fed_mortgage_interest = jubilee_annual_interest  # Under $750K cap
jubilee_fed_salt = 10_000  # Capped at $10K
jubilee_fed_total_itemized = jubilee_fed_mortgage_interest + jubilee_fed_salt

jubilee_fed_incremental = jubilee_fed_total_itemized - STANDARD_DEDUCTION
jubilee_fed_tax_savings_annual = jubilee_fed_incremental * FEDERAL_TAX_RATE
jubilee_fed_tax_savings_monthly = jubilee_fed_tax_savings_annual / 12

print(f"  Mortgage interest:        ${jubilee_fed_mortgage_interest:>10,.0f}")
print(f"  SALT (property tax cap):  ${jubilee_fed_salt:>10,.0f}")
print(f"  Total itemized:           ${jubilee_fed_total_itemized:>10,.0f}")
print(f"  Standard deduction:       ${STANDARD_DEDUCTION:>10,.0f}")
print(f"  Incremental benefit:      ${jubilee_fed_incremental:>10,.0f}")
print(f"  Tax savings @ 32%:        ${jubilee_fed_tax_savings_annual:>10,.0f}/year")
print(f"  MONTHLY TAX BENEFIT:      ${jubilee_fed_tax_savings_monthly:>10,.0f}/month")
print()

jubilee_aftertax = jubilee_pretax - jubilee_fed_tax_savings_monthly

print(f"  Pre-tax monthly:          ${jubilee_pretax:>10,.0f}")
print(f"  Tax benefit:              ${jubilee_fed_tax_savings_monthly:>10,.0f}")
print(f"  AFTER-TAX MONTHLY:        ${jubilee_aftertax:>10,.0f}")
print()

print("TRADITIONAL TAX BENEFIT:")
print("-" * 40)

# Mortgage interest in Year 1
traditional_annual_interest = TRADITIONAL_LOAN * TRADITIONAL_RATE
traditional_capped_interest = 750_000 * TRADITIONAL_RATE  # Only first $750K deductible

print(f"  Year 1 mortgage interest (full): ${traditional_annual_interest:>10,.0f}")
print(f"  Deductible (first $750K):        ${traditional_capped_interest:>10,.0f}")

traditional_fed_mortgage_interest = traditional_capped_interest
traditional_fed_salt = 10_000
traditional_fed_total_itemized = traditional_fed_mortgage_interest + traditional_fed_salt

traditional_fed_incremental = traditional_fed_total_itemized - STANDARD_DEDUCTION
traditional_fed_tax_savings_annual = traditional_fed_incremental * FEDERAL_TAX_RATE
traditional_fed_tax_savings_monthly = traditional_fed_tax_savings_annual / 12

print(f"  Mortgage interest:        ${traditional_fed_mortgage_interest:>10,.0f}")
print(f"  SALT (property tax cap):  ${traditional_fed_salt:>10,.0f}")
print(f"  Total itemized:           ${traditional_fed_total_itemized:>10,.0f}")
print(f"  Standard deduction:       ${STANDARD_DEDUCTION:>10,.0f}")
print(f"  Incremental benefit:      ${traditional_fed_incremental:>10,.0f}")
print(f"  Tax savings @ 32%:        ${traditional_fed_tax_savings_annual:>10,.0f}/year")
print(f"  MONTHLY TAX BENEFIT:      ${traditional_fed_tax_savings_monthly:>10,.0f}/month")
print()

traditional_aftertax = traditional_pretax - traditional_fed_tax_savings_monthly

print(f"  Pre-tax monthly:          ${traditional_pretax:>10,.0f}")
print(f"  Tax benefit:              ${traditional_fed_tax_savings_monthly:>10,.0f}")
print(f"  AFTER-TAX MONTHLY:        ${traditional_aftertax:>10,.0f}")
print()

print("RENTING TAX BENEFIT:")
print("-" * 40)
print(f"  Takes standard deduction")
print(f"  No incremental benefit:   $         0/month")
print(f"  AFTER-TAX MONTHLY:        ${renting_total:>10,.0f}")
print()

# ============================================================================
# CHECK 3: MONTHLY SAVINGS & INVESTMENT GROWTH
# ============================================================================

print("=" * 80)
print("CHECK 3: INVESTMENT GROWTH (Year 1, Month by Month)")
print("=" * 80)
print()

# Initial capital (start of Year 1 = end of Year 5 from previous analysis)
jubilee_portfolio = 379_000
traditional_portfolio = 9_000
renting_portfolio = 439_000

print(f"Starting capital (beginning of Year 1):")
print(f"  Jubilee:     ${jubilee_portfolio:>12,.0f}")
print(f"  Traditional: ${traditional_portfolio:>12,.0f}")
print(f"  Renting:     ${renting_portfolio:>12,.0f}")
print()

# Baseline = most expensive (Jubilee)
baseline_monthly = jubilee_aftertax

print(f"Baseline (most expensive): ${baseline_monthly:,.0f}/month (Jubilee)")
print()

print(f"Monthly savings to invest:")
jubilee_monthly_savings = 0  # Jubilee is the baseline
traditional_monthly_savings = baseline_monthly - traditional_aftertax
renting_monthly_savings = baseline_monthly - renting_total

print(f"  Jubilee:     ${jubilee_monthly_savings:>10,.0f}/month (baseline)")
print(f"  Traditional: ${traditional_monthly_savings:>10,.0f}/month (saves vs baseline)")
print(f"  Renting:     ${renting_monthly_savings:>10,.0f}/month (saves vs baseline)")
print()

print("Month-by-month compounding @ 7% annual (0.5833% monthly):")
print("-" * 80)
print(f"{'Month':<8} {'Jubilee Portfolio':>20} {'Traditional Portfolio':>22} {'Renting Portfolio':>20}")
print("-" * 80)

# Simulate 12 months
for month in range(1, 13):
    # Add monthly savings
    jubilee_portfolio += jubilee_monthly_savings
    traditional_portfolio += traditional_monthly_savings
    renting_portfolio += renting_monthly_savings

    # Compound growth
    jubilee_portfolio *= (1 + MONTHLY_RETURN)
    traditional_portfolio *= (1 + MONTHLY_RETURN)
    renting_portfolio *= (1 + MONTHLY_RETURN)

    if month == 1 or month == 6 or month == 12:
        print(f"{month:<8} ${jubilee_portfolio:>19,.0f} ${traditional_portfolio:>21,.0f} ${renting_portfolio:>19,.0f}")

print()
print(f"Investment portfolio after Year 1:")
print(f"  Jubilee:     ${jubilee_portfolio:>12,.0f}")
print(f"  Traditional: ${traditional_portfolio:>12,.0f}")
print(f"  Renting:     ${renting_portfolio:>12,.0f}")
print()

# ============================================================================
# CHECK 4: HOME VALUE & EQUITY
# ============================================================================

print("=" * 80)
print("CHECK 4: HOME APPRECIATION & EQUITY (End of Year 1)")
print("=" * 80)
print()

# Home appreciation
HOME_APPRECIATION = 0.03
year1_home_value = HOME_PRICE * (1 + HOME_APPRECIATION)

print(f"Home appreciation @ 3%/year:")
print(f"  Start:  ${HOME_PRICE:>12,}")
print(f"  End:    ${year1_home_value:>12,.0f}")
print()

# Mortgage principal paydown (simplified - need to calculate from amortization)
# For 30-year fixed, Year 1 is mostly interest, small principal paydown

def calculate_remaining_balance(principal, annual_rate, monthly_payment, months_paid):
    """Calculate remaining balance after N months of payments"""
    monthly_rate = annual_rate / 12
    n_total = 30 * 12

    remaining_balance = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**months_paid) / \
                       ((1 + monthly_rate)**n_total - 1)
    return remaining_balance

jubilee_remaining = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE, jubilee_mortgage, 12)
jubilee_principal_paid = JUBILEE_LOAN - jubilee_remaining

traditional_remaining = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE, traditional_mortgage, 12)
traditional_principal_paid = TRADITIONAL_LOAN - traditional_remaining

print(f"JUBILEE - Mortgage Principal Paydown:")
print(f"  Starting balance:     ${JUBILEE_LOAN:>12,.0f}")
print(f"  Principal paid (Yr 1): ${jubilee_principal_paid:>12,.0f}")
print(f"  Remaining balance:    ${jubilee_remaining:>12,.0f}")
print()

# Jubilee equity = 40% of (home value - mortgage balance)
jubilee_house_value_end = year1_home_value * 0.40
jubilee_equity = jubilee_house_value_end - jubilee_remaining

print(f"  House value (40%):    ${jubilee_house_value_end:>12,.0f}")
print(f"  Mortgage balance:     ${jubilee_remaining:>12,.0f}")
print(f"  JUBILEE EQUITY:       ${jubilee_equity:>12,.0f}")
print()

print(f"TRADITIONAL - Mortgage Principal Paydown:")
print(f"  Starting balance:     ${TRADITIONAL_LOAN:>12,.0f}")
print(f"  Principal paid (Yr 1): ${traditional_principal_paid:>12,.0f}")
print(f"  Remaining balance:    ${traditional_remaining:>12,.0f}")
print()

traditional_equity = year1_home_value - traditional_remaining

print(f"  Home value (100%):    ${year1_home_value:>12,.0f}")
print(f"  Mortgage balance:     ${traditional_remaining:>12,.0f}")
print(f"  TRADITIONAL EQUITY:   ${traditional_equity:>12,.0f}")
print()

print(f"RENTING - Home Equity:")
print(f"  RENTING EQUITY:       ${0:>12,.0f}")
print()

# ============================================================================
# CHECK 5: NET WORTH AFTER YEAR 1
# ============================================================================

print("=" * 80)
print("CHECK 5: NET WORTH SUMMARY (End of Year 1)")
print("=" * 80)
print()

jubilee_networth = jubilee_portfolio + jubilee_equity
traditional_networth = traditional_portfolio + traditional_equity
renting_networth = renting_portfolio

print(f"{'Scenario':<15} {'Portfolio':>15} {'Home Equity':>15} {'Total Net Worth':>18}")
print("-" * 80)
print(f"{'Jubilee':<15} ${jubilee_portfolio:>14,.0f} ${jubilee_equity:>14,.0f} ${jubilee_networth:>17,.0f}")
print(f"{'Traditional':<15} ${traditional_portfolio:>14,.0f} ${traditional_equity:>14,.0f} ${traditional_networth:>17,.0f}")
print(f"{'Renting':<15} ${renting_portfolio:>14,.0f} ${0:>14,.0f} ${renting_networth:>17,.0f}")
print()

print("=" * 80)
print("DIFFERENCES:")
print("-" * 80)
print(f"Traditional vs Jubilee:  ${traditional_networth - jubilee_networth:>+17,.0f}")
print(f"Renting vs Jubilee:      ${renting_networth - jubilee_networth:>+17,.0f}")
print(f"Traditional vs Renting:  ${traditional_networth - renting_networth:>+17,.0f}")
print()

print("=" * 80)
print("YEAR 1 CHECKS COMPLETE")
print("=" * 80)
print()
print("Please review the above calculations. If they look correct, I will proceed")
print("with the full 50-year analysis.")
