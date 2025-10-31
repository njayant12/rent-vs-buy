#!/usr/bin/env python3
"""
Deep Dive: Jubilee vs Traditional 20% Down (Years 1-30)
Analyzing why Traditional pulls ahead despite Jubilee's $370K head start
"""

import csv

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
LAND_LEASE_INCREASE = 0.03  # After year 5
HOME_APPRECIATION = 0.03

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

# ============================================================================
# SIMULATE 30 YEARS
# ============================================================================

print("=" * 100)
print("DEEP DIVE: JUBILEE VS TRADITIONAL (30 YEARS)")
print("=" * 100)
print()

results = []

jubilee_portfolio = JUBILEE_PORTFOLIO_START
traditional_portfolio = TRADITIONAL_PORTFOLIO_START
home_value = HOME_PRICE

# Track cumulative values
jubilee_cumulative_savings = 0
traditional_cumulative_savings = 0

for year in range(1, 31):
    # Calculate escalated costs
    escalation_factor_2pct = (1 + PROPERTY_TAX_INCREASE) ** (year - 1)
    escalation_factor_3pct = (1 + INSURANCE_INCREASE) ** (year - 1)

    property_tax_monthly = PROPERTY_TAX_Y1 * escalation_factor_2pct
    insurance_monthly = INSURANCE_Y1 * escalation_factor_3pct
    maintenance_monthly = MAINTENANCE_Y1 * escalation_factor_3pct

    # Land lease - fixed years 1-5, then +3% annually
    if year <= 5:
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1
    else:
        years_after_5 = year - 5
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1 * ((1 + LAND_LEASE_INCREASE) ** years_after_5)

    # Mortgage balances at start of year
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

    # Calculate mortgage interest for tax deduction
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
    jubilee_savings = 0  # Jubilee is baseline
    traditional_savings = baseline - traditional_aftertax

    # Track cumulative
    jubilee_cumulative_savings += jubilee_savings * 12
    traditional_cumulative_savings += traditional_savings * 12

    # Simulate 12 months of investment growth
    for month in range(12):
        jubilee_portfolio = (jubilee_portfolio + jubilee_savings) * (1 + MONTHLY_RETURN)
        traditional_portfolio = (traditional_portfolio + traditional_savings) * (1 + MONTHLY_RETURN)

    # Calculate mortgage balances at end of year
    months_paid_end = year * 12
    jubilee_mortgage_balance_end = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE,
                                                               JUBILEE_MORTGAGE, months_paid_end)
    traditional_mortgage_balance_end = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE,
                                                                   TRADITIONAL_MORTGAGE, months_paid_end)

    # Home appreciation
    home_value = home_value * (1 + HOME_APPRECIATION)

    # Calculate equity
    jubilee_house_value = home_value * 0.40
    jubilee_equity = max(0, jubilee_house_value - jubilee_mortgage_balance_end)
    traditional_equity = max(0, home_value - traditional_mortgage_balance_end)

    # Net worth
    jubilee_networth = jubilee_portfolio + jubilee_equity
    traditional_networth = traditional_portfolio + traditional_equity

    # Store results
    results.append({
        'year': year,
        'jubilee_aftertax': jubilee_aftertax,
        'traditional_aftertax': traditional_aftertax,
        'monthly_diff': traditional_aftertax - jubilee_aftertax,
        'traditional_monthly_savings': traditional_savings,
        'jubilee_portfolio': jubilee_portfolio,
        'traditional_portfolio': traditional_portfolio,
        'portfolio_diff': traditional_portfolio - jubilee_portfolio,
        'jubilee_equity': jubilee_equity,
        'traditional_equity': traditional_equity,
        'equity_diff': traditional_equity - jubilee_equity,
        'jubilee_networth': jubilee_networth,
        'traditional_networth': traditional_networth,
        'networth_diff': traditional_networth - jubilee_networth,
        'home_value': home_value,
        'land_lease': land_lease_monthly,
        'jubilee_mortgage_balance': jubilee_mortgage_balance_end,
        'traditional_mortgage_balance': traditional_mortgage_balance_end,
    })

# ============================================================================
# KEY YEARS ANALYSIS
# ============================================================================

print("KEY YEARS DETAILED COMPARISON")
print("=" * 100)
print()

key_years = [1, 5, 6, 10, 20, 30]

for year_num in key_years:
    result = results[year_num - 1]

    print(f"{'=' * 100}")
    print(f"YEAR {year_num}" + (" (Land lease starts escalating)" if year_num == 6 else "") +
          (" (Mortgages paid off)" if year_num == 30 else ""))
    print(f"{'=' * 100}")
    print()

    print(f"MONTHLY COSTS:")
    print(f"  Jubilee after-tax:     ${result['jubilee_aftertax']:>10,.0f}/month")
    print(f"  Traditional after-tax: ${result['traditional_aftertax']:>10,.0f}/month")
    print(f"  Traditional saves:     ${result['traditional_monthly_savings']:>10,.0f}/month")
    print(f"  Land lease (Jubilee):  ${result['land_lease']:>10,.0f}/month")
    print()

    print(f"INVESTMENT PORTFOLIOS:")
    print(f"  Jubilee:               ${result['jubilee_portfolio']:>15,.0f}")
    print(f"  Traditional:           ${result['traditional_portfolio']:>15,.0f}")
    print(f"  Gap:                   ${result['portfolio_diff']:>15,.0f} ({'Traditional ahead' if result['portfolio_diff'] > 0 else 'Jubilee ahead'})")
    print()

    print(f"HOME EQUITY:")
    print(f"  Home value:            ${result['home_value']:>15,.0f}")
    print(f"  Jubilee (40%):         ${result['jubilee_equity']:>15,.0f}")
    print(f"  Traditional (100%):    ${result['traditional_equity']:>15,.0f}")
    print(f"  Gap:                   ${result['equity_diff']:>15,.0f} (Traditional ahead)")
    print()

    print(f"TOTAL NET WORTH:")
    print(f"  Jubilee:               ${result['jubilee_networth']:>15,.0f}")
    print(f"  Traditional:           ${result['traditional_networth']:>15,.0f}")
    print(f"  Gap:                   ${result['networth_diff']:>15,.0f} ({'Traditional ahead' if result['networth_diff'] > 0 else 'Jubilee ahead'})")
    print()
    print()

# ============================================================================
# THE CATCHING UP ANALYSIS
# ============================================================================

print("=" * 100)
print("THE CATCHING UP STORY: Why Traditional Overtakes Jubilee's Head Start")
print("=" * 100)
print()

print("JUBILEE'S STARTING ADVANTAGE:")
print(f"  Portfolio advantage at Year 1 start: ${JUBILEE_PORTFOLIO_START - TRADITIONAL_PORTFOLIO_START:,.0f}")
print()

# Find when Traditional's portfolio catches up
portfolio_catchup = None
for result in results:
    if result['traditional_portfolio'] > result['jubilee_portfolio']:
        portfolio_catchup = result['year']
        break

if portfolio_catchup:
    result = results[portfolio_catchup - 1]
    print(f"PORTFOLIO CROSSOVER: Year {portfolio_catchup}")
    print(f"  Traditional's portfolio finally exceeds Jubilee's!")
    print(f"  Traditional: ${result['traditional_portfolio']:,.0f}")
    print(f"  Jubilee:     ${result['jubilee_portfolio']:,.0f}")
    print()

# Find when Traditional's net worth catches up
networth_catchup = None
for result in results:
    if result['traditional_networth'] > result['jubilee_networth']:
        networth_catchup = result['year']
        break

if networth_catchup:
    result = results[networth_catchup - 1]
    print(f"NET WORTH CROSSOVER: Year {networth_catchup}")
    print(f"  Traditional's total net worth exceeds Jubilee!")
    print(f"  Traditional: ${result['traditional_networth']:,.0f} (Portfolio: ${result['traditional_portfolio']:,.0f}, Equity: ${result['traditional_equity']:,.0f})")
    print(f"  Jubilee:     ${result['jubilee_networth']:,.0f} (Portfolio: ${result['jubilee_portfolio']:,.0f}, Equity: ${result['jubilee_equity']:,.0f})")
    print()

# ============================================================================
# THE THREE ADVANTAGES BREAKDOWN
# ============================================================================

print("=" * 100)
print("TRADITIONAL'S THREE COMPOUNDING ADVANTAGES (After 30 Years)")
print("=" * 100)
print()

result_30 = results[29]

print(f"1. MONTHLY SAVINGS ADVANTAGE:")
print(f"   Traditional saves ${result_30['traditional_monthly_savings']:,.0f}/month consistently")
print(f"   Over 30 years @ 7% return: ${result_30['traditional_portfolio'] - TRADITIONAL_PORTFOLIO_START:,.0f}")
print()

print(f"2. OWNERSHIP ADVANTAGE:")
print(f"   Traditional owns 100% vs Jubilee's 40%")
print(f"   Traditional equity: ${result_30['traditional_equity']:,.0f}")
print(f"   Jubilee equity:     ${result_30['jubilee_equity']:,.0f}")
print(f"   Equity gap:         ${result_30['equity_diff']:,.0f}")
print()

print(f"3. LAND LEASE ESCALATION:")
print(f"   Jubilee's land lease: $6,650/month (Year 1) → ${result_30['land_lease']:,.0f}/month (Year 30)")
print(f"   Total increase: ${(result_30['land_lease'] - JUBILEE_LAND_LEASE_Y1):,.0f}/month ({((result_30['land_lease']/JUBILEE_LAND_LEASE_Y1 - 1)*100):.1f}% higher)")
print()

print(f"COMBINED EFFECT:")
print(f"  Jubilee started with ${JUBILEE_PORTFOLIO_START - TRADITIONAL_PORTFOLIO_START:,.0f} portfolio advantage")
print(f"  Traditional ends with ${result_30['networth_diff']:,.0f} net worth advantage")
print(f"  Total swing: ${result_30['networth_diff'] + (JUBILEE_PORTFOLIO_START - TRADITIONAL_PORTFOLIO_START):,.0f}")
print()

# ============================================================================
# WRITE DETAILED CSV
# ============================================================================

csv_filename = 'jubilee_vs_traditional_30_years.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Jubilee_NetWorth', 'Traditional_NetWorth', 'Gap',
                     'Jubilee_Portfolio', 'Traditional_Portfolio', 'Portfolio_Gap',
                     'Jubilee_Equity', 'Traditional_Equity', 'Equity_Gap',
                     'Land_Lease_Monthly'])
    for result in results:
        writer.writerow([
            result['year'],
            int(result['jubilee_networth']),
            int(result['traditional_networth']),
            int(result['networth_diff']),
            int(result['jubilee_portfolio']),
            int(result['traditional_portfolio']),
            int(result['portfolio_diff']),
            int(result['jubilee_equity']),
            int(result['traditional_equity']),
            int(result['equity_diff']),
            int(result['land_lease'])
        ])

print(f"Detailed CSV written to: {csv_filename}")
print()
