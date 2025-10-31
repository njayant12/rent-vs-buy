#!/usr/bin/env python3
"""
Full 50-Year Net Worth Analysis
Jubilee vs Traditional 20% Down vs Renting
Federal tax benefits only
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
JUBILEE_MORTGAGE = 4_595  # Fixed 30-year
JUBILEE_PMI = 336  # Fixed for life of loan
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
LAND_LEASE_INCREASE = 0.03  # 3% annually (after year 5)
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

MORTGAGE_TERM_YEARS = 30

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_remaining_balance(principal, annual_rate, monthly_payment, months_paid):
    """Calculate remaining mortgage balance after N months"""
    if months_paid >= 360:  # 30 years
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

# ============================================================================
# SIMULATE 50 YEARS
# ============================================================================

print("=" * 90)
print("50-YEAR NET WORTH ANALYSIS")
print("=" * 90)
print()
print("Running simulation...")
print()

results = []

# Initialize
jubilee_portfolio = JUBILEE_PORTFOLIO_START
traditional_portfolio = TRADITIONAL_PORTFOLIO_START
renting_portfolio = RENTING_PORTFOLIO_START
home_value = HOME_PRICE

for year in range(1, 51):
    # Calculate escalated costs for this year
    escalation_factor_2pct = (1 + PROPERTY_TAX_INCREASE) ** (year - 1)
    escalation_factor_3pct = (1 + RENT_INCREASE) ** (year - 1)

    property_tax_monthly = PROPERTY_TAX_Y1 * escalation_factor_2pct
    insurance_monthly = INSURANCE_Y1 * escalation_factor_3pct
    maintenance_monthly = MAINTENANCE_Y1 * escalation_factor_3pct
    rent_monthly = RENT_Y1 * escalation_factor_3pct
    renters_insurance_monthly = RENTERS_INSURANCE_Y1 * escalation_factor_3pct

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

    # Mortgage payments (zero after 30 years)
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

    # Traditional can only deduct interest on first $750K
    traditional_deductible_balance = min(traditional_mortgage_balance_start, MORTGAGE_DEBT_CAP)
    traditional_interest_annual = calculate_mortgage_interest(traditional_deductible_balance, TRADITIONAL_RATE)

    # Monthly costs
    jubilee_pretax = (jubilee_mortgage_payment + jubilee_pmi_payment + land_lease_monthly +
                     property_tax_monthly + insurance_monthly + maintenance_monthly)
    traditional_pretax = (traditional_mortgage_payment + property_tax_monthly +
                         insurance_monthly + maintenance_monthly)
    renting_total = rent_monthly + renters_insurance_monthly

    # Tax benefits
    property_tax_annual = property_tax_monthly * 12
    jubilee_tax_benefit = calculate_tax_benefit(jubilee_interest_annual, property_tax_annual)
    traditional_tax_benefit = calculate_tax_benefit(traditional_interest_annual, property_tax_annual)

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

    # Calculate mortgage balances at end of year
    months_paid_end = year * 12
    jubilee_mortgage_balance_end = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE,
                                                               JUBILEE_MORTGAGE, months_paid_end)
    traditional_mortgage_balance_end = calculate_remaining_balance(TRADITIONAL_LOAN, TRADITIONAL_RATE,
                                                                   TRADITIONAL_MORTGAGE, months_paid_end)

    # Home appreciation
    home_value = home_value * (1 + HOME_APPRECIATION)

    # Calculate equity
    jubilee_house_value = home_value * 0.40  # Jubilee owns 40%
    jubilee_equity = max(0, jubilee_house_value - jubilee_mortgage_balance_end)
    traditional_equity = max(0, home_value - traditional_mortgage_balance_end)
    renting_equity = 0

    # Net worth
    jubilee_networth = jubilee_portfolio + jubilee_equity
    traditional_networth = traditional_portfolio + traditional_equity
    renting_networth = renting_portfolio

    # Store results
    results.append({
        'year': year,
        'jubilee_networth': jubilee_networth,
        'traditional_networth': traditional_networth,
        'renting_networth': renting_networth,
        'jubilee_portfolio': jubilee_portfolio,
        'traditional_portfolio': traditional_portfolio,
        'renting_portfolio': renting_portfolio,
        'jubilee_equity': jubilee_equity,
        'traditional_equity': traditional_equity,
        'jubilee_aftertax': jubilee_aftertax,
        'traditional_aftertax': traditional_aftertax,
        'renting_aftertax': renting_aftertax,
        'home_value': home_value,
        'land_lease': land_lease_monthly,
    })

    # Progress indicator
    if year % 10 == 0:
        print(f"  Year {year}: Jubilee ${jubilee_networth:,.0f} | Traditional ${traditional_networth:,.0f} | Renting ${renting_networth:,.0f}")

print()
print("Simulation complete!")
print()

# ============================================================================
# WRITE CSV FOR GRAPHING
# ============================================================================

csv_filename = 'net_worth_50_years.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Jubilee', 'Traditional', 'Renting'])
    for result in results:
        writer.writerow([
            result['year'],
            int(result['jubilee_networth']),
            int(result['traditional_networth']),
            int(result['renting_networth'])
        ])

print(f"CSV data written to: {csv_filename}")
print()

# ============================================================================
# FIND CROSSOVER POINTS
# ============================================================================

print("=" * 90)
print("CROSSOVER ANALYSIS")
print("=" * 90)
print()

# Check if Traditional ever falls behind Jubilee
trad_beats_jubilee = True
crossover_trad_jub = None
for i, result in enumerate(results):
    if result['jubilee_networth'] > result['traditional_networth']:
        trad_beats_jubilee = False
        crossover_trad_jub = result['year']
        break

if trad_beats_jubilee:
    print("Traditional ALWAYS leads Jubilee (no crossover)")
else:
    print(f"Jubilee catches up to Traditional in Year {crossover_trad_jub}")

# Check if Traditional ever catches up to Renting
trad_catches_renting = False
crossover_trad_rent = None
for result in results:
    if result['traditional_networth'] > result['renting_networth']:
        trad_catches_renting = True
        crossover_trad_rent = result['year']
        break

if trad_catches_renting:
    print(f"Traditional catches up to Renting in Year {crossover_trad_rent}")
else:
    print("Traditional NEVER catches up to Renting")

# Check if Jubilee ever catches up to Renting
jub_catches_renting = False
crossover_jub_rent = None
for result in results:
    if result['jubilee_networth'] > result['renting_networth']:
        jub_catches_renting = True
        crossover_jub_rent = result['year']
        break

if jub_catches_renting:
    print(f"Jubilee catches up to Renting in Year {crossover_jub_rent}")
else:
    print("Jubilee NEVER catches up to Renting")

print()

# ============================================================================
# KEY MILESTONES
# ============================================================================

print("=" * 90)
print("KEY MILESTONES")
print("=" * 90)
print()

# Year 10
result_10 = results[9]
print(f"YEAR 10:")
print(f"  Renting:     ${result_10['renting_networth']:>15,.0f}")
print(f"  Traditional: ${result_10['traditional_networth']:>15,.0f} (diff: ${result_10['traditional_networth']-result_10['renting_networth']:>+12,.0f})")
print(f"  Jubilee:     ${result_10['jubilee_networth']:>15,.0f} (diff: ${result_10['jubilee_networth']-result_10['renting_networth']:>+12,.0f})")
print()

# Year 30 (mortgages paid off)
result_30 = results[29]
print(f"YEAR 30 (Mortgages paid off):")
print(f"  Renting:     ${result_30['renting_networth']:>15,.0f}")
print(f"  Traditional: ${result_30['traditional_networth']:>15,.0f} (diff: ${result_30['traditional_networth']-result_30['renting_networth']:>+12,.0f})")
print(f"  Jubilee:     ${result_30['jubilee_networth']:>15,.0f} (diff: ${result_30['jubilee_networth']-result_30['renting_networth']:>+12,.0f})")
print()

# Year 50 (final)
result_50 = results[49]
print(f"YEAR 50 (Final):")
print(f"  Renting:     ${result_50['renting_networth']:>15,.0f}")
print(f"  Traditional: ${result_50['traditional_networth']:>15,.0f} (diff: ${result_50['traditional_networth']-result_50['renting_networth']:>+12,.0f})")
print(f"  Jubilee:     ${result_50['jubilee_networth']:>15,.0f} (diff: ${result_50['jubilee_networth']-result_50['renting_networth']:>+12,.0f})")
print()

# ============================================================================
# FINAL BREAKDOWN
# ============================================================================

print("=" * 90)
print("YEAR 50 DETAILED BREAKDOWN")
print("=" * 90)
print()

print(f"{'Scenario':<15} {'Portfolio':>18} {'Home Equity':>18} {'Total Net Worth':>20}")
print("-" * 90)
print(f"{'Jubilee':<15} ${result_50['jubilee_portfolio']:>17,.0f} ${result_50['jubilee_equity']:>17,.0f} ${result_50['jubilee_networth']:>19,.0f}")
print(f"{'Traditional':<15} ${result_50['traditional_portfolio']:>17,.0f} ${result_50['traditional_equity']:>17,.0f} ${result_50['traditional_networth']:>19,.0f}")
print(f"{'Renting':<15} ${result_50['renting_portfolio']:>17,.0f} ${0:>17,.0f} ${result_50['renting_networth']:>19,.0f}")
print()

print(f"Home value after 50 years: ${result_50['home_value']:,.0f}")
print(f"Land lease (Jubilee) in Year 50: ${result_50['land_lease']:,.0f}/month")
print()

# ============================================================================
# WINNER
# ============================================================================

print("=" * 90)
print("FINAL RANKING")
print("=" * 90)
print()

rankings = [
    ('Renting', result_50['renting_networth']),
    ('Traditional', result_50['traditional_networth']),
    ('Jubilee', result_50['jubilee_networth'])
]
rankings.sort(key=lambda x: x[1], reverse=True)

medals = ['🥇', '🥈', '🥉']
for i, (name, networth) in enumerate(rankings):
    print(f"{medals[i]} {name:12} ${networth:>15,.0f}")

print()
print("=" * 90)
