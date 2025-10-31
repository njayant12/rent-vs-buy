#!/usr/bin/env python3
"""
Break-Even Analysis: What stock return does Jubilee need to beat Traditional?
Tests different return rates to find where Jubilee catches up
"""

import math

# ============================================================================
# INITIAL VALUES
# ============================================================================

HOME_PRICE = 1_900_000

# Loans (FIXED)
JUBILEE_LOAN = 746_234
TRADITIONAL_LOAN = 1_520_000

# Interest rates
JUBILEE_RATE = 0.0625
TRADITIONAL_RATE = 0.0615

# Fixed monthly costs
JUBILEE_MORTGAGE = 4_595
JUBILEE_PMI = 336
TRADITIONAL_MORTGAGE = 9_260

# Year 1 baseline costs
JUBILEE_LAND_LEASE_Y1 = 6_650
PROPERTY_TAX_Y1 = 1_868
INSURANCE_Y1 = 125
MAINTENANCE_Y1 = 675

# Escalation rates
PROPERTY_TAX_INCREASE = 0.02
INSURANCE_INCREASE = 0.03
MAINTENANCE_INCREASE = 0.03
LAND_LEASE_INCREASE = 0.03
HOME_APPRECIATION = 0.03

# Tax rates (FEDERAL ONLY)
FEDERAL_TAX_RATE = 0.32
STANDARD_DEDUCTION = 29_200
SALT_CAP = 10_000
MORTGAGE_DEBT_CAP = 750_000

# Starting portfolios
JUBILEE_PORTFOLIO_START = 379_000
TRADITIONAL_PORTFOLIO_START = 9_000

MORTGAGE_TERM_YEARS = 30

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_remaining_balance(principal, annual_rate, monthly_payment, months_paid):
    """Calculate remaining mortgage balance after N months"""
    if months_paid >= 360:
        return 0
    monthly_rate = annual_rate / 12
    n_total = 30 * 12
    remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**months_paid) / \
                ((1 + monthly_rate)**n_total - 1)
    return remaining

def calculate_mortgage_interest(remaining_balance, annual_rate):
    """Calculate annual mortgage interest for current year"""
    return remaining_balance * annual_rate

def calculate_tax_benefit(mortgage_interest_annual, property_tax_annual):
    """Calculate federal tax benefit"""
    deductible_interest = mortgage_interest_annual
    deductible_salt = min(property_tax_annual, SALT_CAP)
    total_itemized = deductible_interest + deductible_salt
    incremental = max(0, total_itemized - STANDARD_DEDUCTION)
    tax_savings_annual = incremental * FEDERAL_TAX_RATE
    tax_savings_monthly = tax_savings_annual / 12
    return tax_savings_monthly

def simulate_scenario(annual_return, years):
    """Simulate both scenarios with given return rate for N years"""
    monthly_return = annual_return / 12

    jubilee_portfolio = JUBILEE_PORTFOLIO_START
    traditional_portfolio = TRADITIONAL_PORTFOLIO_START
    home_value = HOME_PRICE

    for year in range(1, years + 1):
        # Calculate escalated costs
        escalation_factor_2pct = (1 + PROPERTY_TAX_INCREASE) ** (year - 1)
        escalation_factor_3pct = (1 + INSURANCE_INCREASE) ** (year - 1)

        property_tax_monthly = PROPERTY_TAX_Y1 * escalation_factor_2pct
        insurance_monthly = INSURANCE_Y1 * escalation_factor_3pct
        maintenance_monthly = MAINTENANCE_Y1 * escalation_factor_3pct

        # Land lease
        if year <= 5:
            land_lease_monthly = JUBILEE_LAND_LEASE_Y1
        else:
            years_after_5 = year - 5
            land_lease_monthly = JUBILEE_LAND_LEASE_Y1 * ((1 + LAND_LEASE_INCREASE) ** years_after_5)

        # Mortgage balances
        months_paid_start = (year - 1) * 12
        jubilee_mortgage_balance_start = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE,
                                                                     JUBILEE_MORTGAGE, months_paid_start)
        traditional_mortgage_balance_start = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE,
                                                                         TRADITIONAL_MORTGAGE, months_paid_start)

        # Mortgage payments
        if year <= MORTGAGE_TERM_YEARS:
            jubilee_mortgage_payment = JUBILEE_MORTGAGE
            jubilee_pmi_payment = JUBILEE_PMI
            traditional_mortgage_payment = TRADITIONAL_MORTGAGE
        else:
            jubilee_mortgage_payment = 0
            jubilee_pmi_payment = 0
            traditional_mortgage_payment = 0

        # Calculate interest for tax deduction
        jubilee_interest_annual = calculate_mortgage_interest(jubilee_mortgage_balance_start, JUBILEE_RATE)
        traditional_deductible_balance = min(traditional_mortgage_balance_start, MORTGAGE_DEBT_CAP)
        traditional_interest_annual = calculate_mortgage_interest(traditional_deductible_balance, TRADITIONAL_RATE)

        # Monthly costs
        jubilee_pretax = (jubilee_mortgage_payment + jubilee_pmi_payment + land_lease_monthly +
                         property_tax_monthly + insurance_monthly + maintenance_monthly)
        traditional_pretax = (traditional_mortgage_payment + property_tax_monthly +
                             insurance_monthly + maintenance_monthly)

        # Tax benefits
        property_tax_annual = property_tax_monthly * 12
        jubilee_tax_benefit = calculate_tax_benefit(jubilee_interest_annual, property_tax_annual)
        traditional_tax_benefit = calculate_tax_benefit(traditional_interest_annual, property_tax_annual)

        # After-tax costs
        jubilee_aftertax = jubilee_pretax - jubilee_tax_benefit
        traditional_aftertax = traditional_pretax - traditional_tax_benefit

        # Monthly savings (using Jubilee as baseline)
        baseline = jubilee_aftertax
        jubilee_savings = 0
        traditional_savings = baseline - traditional_aftertax

        # Simulate 12 months of investment growth
        for month in range(12):
            jubilee_portfolio = (jubilee_portfolio + jubilee_savings) * (1 + monthly_return)
            traditional_portfolio = (traditional_portfolio + traditional_savings) * (1 + monthly_return)

        # Calculate mortgage balances at end of year
        months_paid_end = year * 12
        jubilee_mortgage_balance_end = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE,
                                                                   JUBILEE_MORTGAGE, months_paid_end)
        traditional_mortgage_balance_end = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE,
                                                                       TRADITIONAL_MORTGAGE, months_paid_end)

        # Home appreciation
        home_value = home_value * (1 + HOME_APPRECIATION)

    # Final calculation
    jubilee_house_value = home_value * 0.40
    jubilee_equity = max(0, jubilee_house_value - jubilee_mortgage_balance_end)
    traditional_equity = max(0, home_value - traditional_mortgage_balance_end)

    jubilee_networth = jubilee_portfolio + jubilee_equity
    traditional_networth = traditional_portfolio + traditional_equity

    return {
        'jubilee_networth': jubilee_networth,
        'traditional_networth': traditional_networth,
        'jubilee_portfolio': jubilee_portfolio,
        'traditional_portfolio': traditional_portfolio,
        'jubilee_equity': jubilee_equity,
        'traditional_equity': traditional_equity,
        'home_value': home_value,
    }

# ============================================================================
# BINARY SEARCH FOR BREAK-EVEN RETURN
# ============================================================================

def find_breakeven_return(years, tolerance=0.0001):
    """Binary search to find the return rate where Jubilee = Traditional"""
    low = 0.07  # Start at 7%
    high = 0.30  # Max search at 30%

    while high - low > tolerance:
        mid = (low + high) / 2
        result = simulate_scenario(mid, years)
        diff = result['jubilee_networth'] - result['traditional_networth']

        if diff < 0:
            # Jubilee behind, needs higher return
            low = mid
        else:
            # Jubilee ahead, can use lower return
            high = mid

    return mid

# ============================================================================
# RUN ANALYSIS
# ============================================================================

print("=" * 90)
print("BREAK-EVEN ANALYSIS: Stock Return Needed for Jubilee to Match Traditional")
print("=" * 90)
print()

# Test at different time horizons
horizons = [10, 20, 30]

for years in horizons:
    print(f"{'=' * 90}")
    print(f"YEAR {years} BREAK-EVEN")
    print(f"{'=' * 90}")
    print()

    # Find break-even
    breakeven_rate = find_breakeven_return(years)

    # Get details at break-even
    result = simulate_scenario(breakeven_rate, years)

    print(f"Required annual stock return: {breakeven_rate * 100:.2f}%")
    print()

    print(f"At this return rate:")
    print(f"  Jubilee net worth:     ${result['jubilee_networth']:>15,.0f}")
    print(f"  Traditional net worth: ${result['traditional_networth']:>15,.0f}")
    print(f"  Difference:            ${result['jubilee_networth'] - result['traditional_networth']:>15,.0f}")
    print()

    print(f"Portfolio breakdown:")
    print(f"  Jubilee portfolio:     ${result['jubilee_portfolio']:>15,.0f}")
    print(f"  Traditional portfolio: ${result['traditional_portfolio']:>15,.0f}")
    print(f"  Portfolio gap:         ${result['jubilee_portfolio'] - result['traditional_portfolio']:>15,.0f}")
    print()

    print(f"Equity breakdown:")
    print(f"  Jubilee equity (40%):  ${result['jubilee_equity']:>15,.0f}")
    print(f"  Traditional equity:    ${result['traditional_equity']:>15,.0f}")
    print(f"  Equity gap:            ${result['traditional_equity'] - result['jubilee_equity']:>15,.0f}")
    print()

    print(f"Home value: ${result['home_value']:,.0f}")
    print()
    print()

# ============================================================================
# COMPARISON TABLE AT DIFFERENT RETURNS
# ============================================================================

print("=" * 90)
print("NET WORTH AT YEAR 30 WITH DIFFERENT STOCK RETURNS")
print("=" * 90)
print()

print(f"{'Return Rate':<15} {'Jubilee':>18} {'Traditional':>18} {'Winner':>15} {'Gap':>18}")
print("-" * 90)

test_returns = [0.05, 0.07, 0.10, 0.12, 0.15, 0.20]

for rate in test_returns:
    result = simulate_scenario(rate, 30)
    jub_nw = result['jubilee_networth']
    trad_nw = result['traditional_networth']

    if jub_nw > trad_nw:
        winner = "Jubilee"
        gap = jub_nw - trad_nw
    else:
        winner = "Traditional"
        gap = trad_nw - jub_nw

    print(f"{rate*100:>5.1f}%{'':<9} ${jub_nw:>17,.0f} ${trad_nw:>17,.0f} {winner:>15} ${gap:>17,.0f}")

print()

# ============================================================================
# KEY INSIGHTS
# ============================================================================

print("=" * 90)
print("KEY INSIGHTS")
print("=" * 90)
print()

breakeven_30 = find_breakeven_return(30)

print(f"At current 7% stock return assumption:")
result_7pct = simulate_scenario(0.07, 30)
print(f"  Traditional beats Jubilee by ${result_7pct['traditional_networth'] - result_7pct['jubilee_networth']:,.0f}")
print()

print(f"Jubilee needs {breakeven_30 * 100:.2f}% annual stock return to match Traditional at Year 30")
print(f"That's {(breakeven_30 - 0.07) * 100:.2f} percentage points higher than the 7% baseline")
print()

print(f"Why is such a high return needed?")
print(f"  1. Jubilee saves $0/month (it's the baseline)")
print(f"  2. Traditional saves and invests ~$2-10K/month over 30 years")
print(f"  3. Traditional gets 100% equity vs Jubilee's 40%")
print(f"  4. Land lease escalates from $6,650 to $13,924/month")
print()

print(f"Jubilee's $370K head start needs very high returns to overcome these disadvantages")
print()
