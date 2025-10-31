#!/usr/bin/env python3
"""
Years 1-3 Detailed Check - 50 Year Analysis
Federal tax benefits only (CA tax cancels with standard deduction)
Shows escalation of costs over time
"""

import math

# ============================================================================
# INITIAL VALUES
# ============================================================================

HOME_PRICE = 1_900_000
JUBILEE_HOUSE_VALUE = HOME_PRICE * 0.40
JUBILEE_LAND_VALUE = HOME_PRICE * 0.60

# Loans (FIXED)
JUBILEE_LOAN = 746_234
TRADITIONAL_LOAN = 1_520_000

# Interest rates
JUBILEE_RATE = 0.0625
TRADITIONAL_RATE = 0.0615

# Fixed monthly costs
JUBILEE_MORTGAGE = 4_595  # Fixed 30-year
JUBILEE_PMI = 336  # Fixed
TRADITIONAL_MORTGAGE = 9_260  # Fixed 30-year

# Year 1 baseline costs
JUBILEE_LAND_LEASE_Y1 = 6_650  # Fixed years 1-5
PROPERTY_TAX_Y1 = 1_868
INSURANCE_Y1 = 125
MAINTENANCE_Y1 = 675
RENT_Y1 = 5_800
RENTERS_INSURANCE_Y1 = 17

# Escalation rates
PROPERTY_TAX_INCREASE = 0.02  # 2% annually
RENT_INCREASE = 0.03  # 3% annually
INSURANCE_INCREASE = 0.03  # 3% annually
MAINTENANCE_INCREASE = 0.03  # 3% annually
LAND_LEASE_INCREASE = 0.03  # 3% annually (but only after year 5)
HOME_APPRECIATION = 0.03  # 3% annually

# Tax rates (FEDERAL ONLY)
FEDERAL_TAX_RATE = 0.32
STANDARD_DEDUCTION = 29_200
SALT_CAP = 10_000
MORTGAGE_DEBT_CAP = 750_000

# Investment return
ANNUAL_RETURN = 0.07
MONTHLY_RETURN = ANNUAL_RETURN / 12

# Starting portfolios
JUBILEE_PORTFOLIO_START = 379_000
TRADITIONAL_PORTFOLIO_START = 9_000
RENTING_PORTFOLIO_START = 439_000

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_remaining_balance(principal, annual_rate, monthly_payment, months_paid):
    """Calculate remaining mortgage balance after N months"""
    monthly_rate = annual_rate / 12
    n_total = 30 * 12

    remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**months_paid) / \
                ((1 + monthly_rate)**n_total - 1)
    return remaining

def calculate_tax_benefit(mortgage_interest_annual, property_tax_annual):
    """Calculate federal tax benefit (incremental above standard deduction)"""
    # Cap mortgage interest at $750K debt limit
    deductible_interest = mortgage_interest_annual

    # Cap SALT at $10K
    deductible_salt = min(property_tax_annual, SALT_CAP)

    # Total itemized
    total_itemized = deductible_interest + deductible_salt

    # Incremental benefit vs standard deduction
    incremental = max(0, total_itemized - STANDARD_DEDUCTION)

    # Tax savings
    tax_savings_annual = incremental * FEDERAL_TAX_RATE
    tax_savings_monthly = tax_savings_annual / 12

    return tax_savings_monthly

def simulate_year(year_num, jubilee_portfolio, traditional_portfolio, renting_portfolio,
                 jubilee_mortgage_balance, traditional_mortgage_balance, home_value):
    """Simulate one year and return ending values"""

    # Calculate escalated costs for this year
    escalation_factor_2pct = (1 + PROPERTY_TAX_INCREASE) ** (year_num - 1)
    escalation_factor_3pct = (1 + RENT_INCREASE) ** (year_num - 1)

    property_tax_monthly = PROPERTY_TAX_Y1 * escalation_factor_2pct
    insurance_monthly = INSURANCE_Y1 * escalation_factor_3pct
    maintenance_monthly = MAINTENANCE_Y1 * escalation_factor_3pct
    rent_monthly = RENT_Y1 * escalation_factor_3pct
    renters_insurance_monthly = RENTERS_INSURANCE_Y1 * escalation_factor_3pct

    # Land lease - fixed years 1-5, then +3% annually
    if year_num <= 5:
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1
    else:
        years_after_5 = year_num - 5
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1 * ((1 + LAND_LEASE_INCREASE) ** years_after_5)

    # Calculate mortgage interest for this year
    months_into_mortgage = (year_num - 1) * 12
    jubilee_interest_year_start = jubilee_mortgage_balance * JUBILEE_RATE
    traditional_interest_year_start = min(traditional_mortgage_balance, MORTGAGE_DEBT_CAP) * TRADITIONAL_RATE

    # Monthly costs
    jubilee_pretax = (JUBILEE_MORTGAGE + JUBILEE_PMI + land_lease_monthly +
                     property_tax_monthly + insurance_monthly + maintenance_monthly)
    traditional_pretax = (TRADITIONAL_MORTGAGE + property_tax_monthly +
                         insurance_monthly + maintenance_monthly)
    renting_total = rent_monthly + renters_insurance_monthly

    # Tax benefits
    property_tax_annual = property_tax_monthly * 12
    jubilee_tax_benefit = calculate_tax_benefit(jubilee_interest_year_start, property_tax_annual)
    traditional_tax_benefit = calculate_tax_benefit(traditional_interest_year_start, property_tax_annual)

    # After-tax costs
    jubilee_aftertax = jubilee_pretax - jubilee_tax_benefit
    traditional_aftertax = traditional_pretax - traditional_tax_benefit
    renting_aftertax = renting_total

    # Baseline = most expensive
    baseline = max(jubilee_aftertax, traditional_aftertax, renting_aftertax)

    # Monthly savings
    jubilee_savings = baseline - jubilee_aftertax
    traditional_savings = baseline - traditional_aftertax
    renting_savings = baseline - renting_aftertax

    # Simulate 12 months of investment growth
    for month in range(12):
        jubilee_portfolio = (jubilee_portfolio + jubilee_savings) * (1 + MONTHLY_RETURN)
        traditional_portfolio = (traditional_portfolio + traditional_savings) * (1 + MONTHLY_RETURN)
        renting_portfolio = (renting_portfolio + renting_savings) * (1 + MONTHLY_RETURN)

    # Calculate mortgage paydown
    months_paid = year_num * 12
    jubilee_mortgage_balance_end = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE, JUBILEE_MORTGAGE, months_paid)
    traditional_mortgage_balance_end = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE, TRADITIONAL_MORTGAGE, months_paid)

    jubilee_principal_paid = jubilee_mortgage_balance - jubilee_mortgage_balance_end
    traditional_principal_paid = traditional_mortgage_balance - traditional_mortgage_balance_end

    # Home appreciation
    home_value_end = home_value * (1 + HOME_APPRECIATION)

    # Calculate equity
    jubilee_house_value = home_value_end * 0.40
    jubilee_equity = jubilee_house_value - jubilee_mortgage_balance_end
    traditional_equity = home_value_end - traditional_mortgage_balance_end
    renting_equity = 0

    # Net worth
    jubilee_networth = jubilee_portfolio + jubilee_equity
    traditional_networth = traditional_portfolio + traditional_equity
    renting_networth = renting_portfolio

    return {
        'year': year_num,
        'jubilee': {
            'pretax': jubilee_pretax,
            'tax_benefit': jubilee_tax_benefit,
            'aftertax': jubilee_aftertax,
            'land_lease': land_lease_monthly,
            'property_tax': property_tax_monthly,
            'insurance': insurance_monthly,
            'maintenance': maintenance_monthly,
            'portfolio': jubilee_portfolio,
            'mortgage_balance': jubilee_mortgage_balance_end,
            'principal_paid': jubilee_principal_paid,
            'equity': jubilee_equity,
            'networth': jubilee_networth,
            'monthly_savings': jubilee_savings
        },
        'traditional': {
            'pretax': traditional_pretax,
            'tax_benefit': traditional_tax_benefit,
            'aftertax': traditional_aftertax,
            'property_tax': property_tax_monthly,
            'insurance': insurance_monthly,
            'maintenance': maintenance_monthly,
            'portfolio': traditional_portfolio,
            'mortgage_balance': traditional_mortgage_balance_end,
            'principal_paid': traditional_principal_paid,
            'equity': traditional_equity,
            'networth': traditional_networth,
            'monthly_savings': traditional_savings
        },
        'renting': {
            'total': renting_total,
            'rent': rent_monthly,
            'insurance': renters_insurance_monthly,
            'portfolio': renting_portfolio,
            'networth': renting_networth,
            'monthly_savings': renting_savings
        },
        'home_value': home_value_end,
        'baseline': baseline
    }

# ============================================================================
# SIMULATE YEARS 1-3
# ============================================================================

print("=" * 90)
print("YEARS 1-3 DETAILED CHECK - WITH ESCALATIONS")
print("=" * 90)
print()

results = []
jubilee_portfolio = JUBILEE_PORTFOLIO_START
traditional_portfolio = TRADITIONAL_PORTFOLIO_START
renting_portfolio = RENTING_PORTFOLIO_START
jubilee_mortgage_balance = JUBILEE_LOAN
traditional_mortgage_balance = TRADITIONAL_LOAN
home_value = HOME_PRICE

for year in [1, 2, 3]:
    result = simulate_year(year, jubilee_portfolio, traditional_portfolio, renting_portfolio,
                          jubilee_mortgage_balance, traditional_mortgage_balance, home_value)
    results.append(result)

    # Update for next year
    jubilee_portfolio = result['jubilee']['portfolio']
    traditional_portfolio = result['traditional']['portfolio']
    renting_portfolio = result['renting']['portfolio']
    jubilee_mortgage_balance = result['jubilee']['mortgage_balance']
    traditional_mortgage_balance = result['traditional']['mortgage_balance']
    home_value = result['home_value']

# ============================================================================
# DISPLAY RESULTS
# ============================================================================

for result in results:
    year = result['year']
    print(f"{'=' * 90}")
    print(f"YEAR {year} SUMMARY")
    print(f"{'=' * 90}")
    print()

    print(f"HOME VALUE: ${result['home_value']:,.0f} (+3% from previous year)")
    print()

    print(f"MONTHLY COSTS:")
    print(f"{'-' * 90}")
    print(f"{'Component':<25} {'Jubilee':>15} {'Traditional':>15} {'Renting':>15}")
    print(f"{'-' * 90}")
    print(f"{'Mortgage P&I':<25} ${JUBILEE_MORTGAGE:>14,} ${TRADITIONAL_MORTGAGE:>14,} ${0:>14,}")
    print(f"{'PMI':<25} ${JUBILEE_PMI:>14,} ${0:>14,} ${0:>14,}")
    print(f"{'Land lease':<25} ${result['jubilee']['land_lease']:>14,.0f} ${0:>14,} ${0:>14,}")
    print(f"{'Rent':<25} ${0:>14,} ${0:>14,} ${result['renting']['rent']:>14,.0f}")
    print(f"{'Property tax':<25} ${result['jubilee']['property_tax']:>14,.0f} ${result['traditional']['property_tax']:>14,.0f} ${0:>14,}")
    print(f"{'Insurance':<25} ${result['jubilee']['insurance']:>14,.0f} ${result['traditional']['insurance']:>14,.0f} ${result['renting']['insurance']:>14,.0f}")
    print(f"{'Maintenance':<25} ${result['jubilee']['maintenance']:>14,.0f} ${result['traditional']['maintenance']:>14,.0f} ${0:>14,}")
    print(f"{'-' * 90}")
    print(f"{'PRE-TAX TOTAL':<25} ${result['jubilee']['pretax']:>14,.0f} ${result['traditional']['pretax']:>14,.0f} ${result['renting']['total']:>14,.0f}")
    print(f"{'Tax benefit':<25} -${result['jubilee']['tax_benefit']:>13,.0f} -${result['traditional']['tax_benefit']:>13,.0f} ${0:>14,}")
    print(f"{'AFTER-TAX TOTAL':<25} ${result['jubilee']['aftertax']:>14,.0f} ${result['traditional']['aftertax']:>14,.0f} ${result['renting']['total']:>14,.0f}")
    print()

    print(f"MONTHLY SAVINGS (vs baseline of ${result['baseline']:,.0f}):")
    print(f"  Jubilee:     ${result['jubilee']['monthly_savings']:>10,.0f}/month")
    print(f"  Traditional: ${result['traditional']['monthly_savings']:>10,.0f}/month")
    print(f"  Renting:     ${result['renting']['monthly_savings']:>10,.0f}/month")
    print()

    print(f"MORTGAGE PRINCIPAL PAYDOWN:")
    print(f"  Jubilee:     ${result['jubilee']['principal_paid']:>10,.0f} (balance: ${result['jubilee']['mortgage_balance']:>12,.0f})")
    print(f"  Traditional: ${result['traditional']['principal_paid']:>10,.0f} (balance: ${result['traditional']['mortgage_balance']:>12,.0f})")
    print()

    print(f"NET WORTH SUMMARY (End of Year {year}):")
    print(f"{'-' * 90}")
    print(f"{'Scenario':<15} {'Portfolio':>18} {'Home Equity':>18} {'Total Net Worth':>20}")
    print(f"{'-' * 90}")
    print(f"{'Jubilee':<15} ${result['jubilee']['portfolio']:>17,.0f} ${result['jubilee']['equity']:>17,.0f} ${result['jubilee']['networth']:>19,.0f}")
    print(f"{'Traditional':<15} ${result['traditional']['portfolio']:>17,.0f} ${result['traditional']['equity']:>17,.0f} ${result['traditional']['networth']:>19,.0f}")
    print(f"{'Renting':<15} ${result['renting']['portfolio']:>17,.0f} ${0:>17,.0f} ${result['renting']['networth']:>19,.0f}")
    print()

    print(f"DIFFERENCES:")
    print(f"  Traditional vs Jubilee:  ${result['traditional']['networth'] - result['jubilee']['networth']:>+17,.0f}")
    print(f"  Renting vs Jubilee:      ${result['renting']['networth'] - result['jubilee']['networth']:>+17,.0f}")
    print(f"  Traditional vs Renting:  ${result['traditional']['networth'] - result['renting']['networth']:>+17,.0f}")
    print()
    print()

print("=" * 90)
print("ESCALATION CHECK:")
print("=" * 90)
print()
print(f"{'Component':<20} {'Year 1':>12} {'Year 2':>12} {'Year 3':>12} {'Rate':>10}")
print(f"{'-' * 90}")
print(f"{'Property tax':<20} ${results[0]['jubilee']['property_tax']:>11,.0f} ${results[1]['jubilee']['property_tax']:>11,.0f} ${results[2]['jubilee']['property_tax']:>11,.0f} {'+2%/yr':>10}")
print(f"{'Insurance':<20} ${results[0]['jubilee']['insurance']:>11,.0f} ${results[1]['jubilee']['insurance']:>11,.0f} ${results[2]['jubilee']['insurance']:>11,.0f} {'+3%/yr':>10}")
print(f"{'Maintenance':<20} ${results[0]['jubilee']['maintenance']:>11,.0f} ${results[1]['jubilee']['maintenance']:>11,.0f} ${results[2]['jubilee']['maintenance']:>11,.0f} {'+3%/yr':>10}")
print(f"{'Rent':<20} ${results[0]['renting']['rent']:>11,.0f} ${results[1]['renting']['rent']:>11,.0f} ${results[2]['renting']['rent']:>11,.0f} {'+3%/yr':>10}")
print(f"{'Land lease (Jub)':<20} ${results[0]['jubilee']['land_lease']:>11,.0f} ${results[1]['jubilee']['land_lease']:>11,.0f} ${results[2]['jubilee']['land_lease']:>11,.0f} {'Fixed 1-5':>10}")
print(f"{'Home value':<20} ${results[0]['home_value']:>11,.0f} ${results[1]['home_value']:>11,.0f} ${results[2]['home_value']:>11,.0f} {'+3%/yr':>10}")
print()
