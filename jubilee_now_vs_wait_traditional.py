#!/usr/bin/env python3
"""
Scenario Comparison: Buy Jubilee NOW vs Save & Wait for Traditional
30-year analysis from TODAY
"""

import csv
import math

# ============================================================================
# CONSTANTS
# ============================================================================

HOME_PRICE_TODAY = 1_900_000
JUBILEE_CLOSING_COSTS = 30_000
TRADITIONAL_CLOSING_COSTS = 30_000

# Down payments
JUBILEE_DOWN_PAYMENT = 27_000  # 3.5% of house value ($760K)
TRADITIONAL_DOWN_PCT = 0.20

# Starting cash
STARTING_CASH = 56_000

# Loans
JUBILEE_LOAN = 746_234  # Includes upfront PMI
JUBILEE_RATE = 0.0625
TRADITIONAL_RATE = 0.0615

# Fixed monthly costs
JUBILEE_MORTGAGE = 4_595
JUBILEE_PMI = 336
TRADITIONAL_MORTGAGE_CALC = lambda loan: loan * (TRADITIONAL_RATE/12) * ((1 + TRADITIONAL_RATE/12)**360) / (((1 + TRADITIONAL_RATE/12)**360) - 1)

# Year 1 costs
JUBILEE_LAND_LEASE_Y1 = 6_650
PROPERTY_TAX_Y1 = 1_868
INSURANCE_Y1 = 125
MAINTENANCE_Y1 = 675
RENT_Y1 = 5_800
RENTERS_INSURANCE_Y1 = 17

# Escalation rates
PROPERTY_TAX_INCREASE = 0.02
INSURANCE_INCREASE = 0.03
MAINTENANCE_INCREASE = 0.03
LAND_LEASE_INCREASE = 0.03
HOME_APPRECIATION = 0.03
RENT_INCREASE = 0.03

# Tax & investment
FEDERAL_TAX_RATE = 0.32
STANDARD_DEDUCTION = 29_200
SALT_CAP = 10_000
MORTGAGE_DEBT_CAP = 750_000
ANNUAL_RETURN = 0.07
MONTHLY_RETURN = ANNUAL_RETURN / 12

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_remaining_balance(principal, annual_rate, monthly_payment, months_paid):
    """Calculate remaining mortgage balance"""
    if months_paid >= 360 or principal == 0:
        return 0
    monthly_rate = annual_rate / 12
    n_total = 360
    remaining = principal * ((1 + monthly_rate)**n_total - (1 + monthly_rate)**months_paid) / \
                ((1 + monthly_rate)**n_total - 1)
    return remaining

def calculate_tax_benefit(mortgage_interest_annual, property_tax_annual):
    """Calculate federal tax benefit"""
    deductible_interest = mortgage_interest_annual
    deductible_salt = min(property_tax_annual, SALT_CAP)
    total_itemized = deductible_interest + deductible_salt
    incremental = max(0, total_itemized - STANDARD_DEDUCTION)
    tax_savings_annual = incremental * FEDERAL_TAX_RATE
    return tax_savings_annual / 12

# ============================================================================
# PHASE 1: HOW LONG TO SAVE $410K?
# ============================================================================

print("=" * 90)
print("PHASE 1: HOW LONG DOES IT TAKE TO SAVE FOR TRADITIONAL DOWN PAYMENT?")
print("=" * 90)
print()

target_cash = HOME_PRICE_TODAY * TRADITIONAL_DOWN_PCT + TRADITIONAL_CLOSING_COSTS
print(f"Target cash needed: ${target_cash:,.0f}")
print(f"  20% down payment: ${HOME_PRICE_TODAY * TRADITIONAL_DOWN_PCT:,.0f}")
print(f"  Closing costs:    ${TRADITIONAL_CLOSING_COSTS:,.0f}")
print()

print(f"Starting cash: ${STARTING_CASH:,.0f}")
print()

# Calculate monthly savings while renting
# Assume they can afford Jubilee-level payments but choose to rent instead
jubilee_y1_cost = 13_517  # From previous analysis
rent_y1_cost = 5_817
monthly_savings = jubilee_y1_cost - rent_y1_cost

print(f"Renting costs: ${rent_y1_cost:,.0f}/month (Year 1)")
print(f"Can afford:    ${jubilee_y1_cost:,.0f}/month (Jubilee baseline)")
print(f"Monthly savings: ${monthly_savings:,.0f}/month")
print()

# Simulate saving until reaching target
portfolio = STARTING_CASH
month = 0
rent_monthly = RENT_Y1
renters_insurance_monthly = RENTERS_INSURANCE_Y1

print("Saving progress:")
while portfolio < target_cash:
    month += 1
    year = (month - 1) // 12 + 1

    # Update rent costs each year
    if month % 12 == 1:
        escalation = (1 + RENT_INCREASE) ** (year - 1)
        rent_monthly = RENT_Y1 * escalation
        renters_insurance_monthly = RENTERS_INSURANCE_Y1 * escalation
        rent_cost = rent_monthly + renters_insurance_monthly

        # Recalculate savings (assuming they keep affording Jubilee baseline)
        # Actually, let's keep savings constant for simplicity
        # monthly_savings stays at ~$7,700

    # Add savings and compound
    portfolio = (portfolio + monthly_savings) * (1 + MONTHLY_RETURN)

    if month % 12 == 0:
        print(f"  Year {year}: ${portfolio:,.0f}")

    if month > 360:  # Safety: max 30 years
        print("  ERROR: Takes more than 30 years to save!")
        break

years_to_save = month / 12
print()
print(f"Time to save ${target_cash:,.0f}: {years_to_save:.1f} years ({month} months)")
print(f"Portfolio when ready to buy: ${portfolio:,.0f}")
print()

# Home price when they buy
home_price_when_buy = HOME_PRICE_TODAY * ((1 + HOME_APPRECIATION) ** years_to_save)
print(f"Home price after {years_to_save:.1f} years @ 3%/year: ${home_price_when_buy:,.0f}")
print()

# Adjust purchase if home appreciated
actual_down_payment = home_price_when_buy * TRADITIONAL_DOWN_PCT
actual_total_needed = actual_down_payment + TRADITIONAL_CLOSING_COSTS
remaining_portfolio_after_purchase = portfolio - actual_total_needed

print(f"Actual purchase details:")
print(f"  Home price:       ${home_price_when_buy:,.0f}")
print(f"  Down payment:     ${actual_down_payment:,.0f}")
print(f"  Closing costs:    ${TRADITIONAL_CLOSING_COSTS:,.0f}")
print(f"  Total needed:     ${actual_total_needed:,.0f}")
print(f"  Portfolio after:  ${remaining_portfolio_after_purchase:,.0f}")
print()

wait_months = month
wait_years = years_to_save

# ============================================================================
# PHASE 2: 30-YEAR SIMULATION FROM TODAY
# ============================================================================

print("=" * 90)
print("PHASE 2: 30-YEAR NET WORTH COMPARISON (FROM TODAY)")
print("=" * 90)
print()

results = []

for year in range(1, 31):
    # ========================================================================
    # SCENARIO A: BUY JUBILEE NOW
    # ========================================================================

    if year == 1:
        # Initialize
        jubilee_portfolio = 0  # Spent all $56K on down payment + closing
        jubilee_mortgage_balance = JUBILEE_LOAN
        jubilee_home_value = HOME_PRICE_TODAY

    # Escalated costs
    escalation_2pct = (1 + PROPERTY_TAX_INCREASE) ** (year - 1)
    escalation_3pct = (1 + INSURANCE_INCREASE) ** (year - 1)

    property_tax_monthly = PROPERTY_TAX_Y1 * escalation_2pct
    insurance_monthly = INSURANCE_Y1 * escalation_3pct
    maintenance_monthly = MAINTENANCE_Y1 * escalation_3pct

    if year <= 5:
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1
    else:
        land_lease_monthly = JUBILEE_LAND_LEASE_Y1 * ((1 + LAND_LEASE_INCREASE) ** (year - 6))

    # Mortgage payment
    if year <= 30:
        jubilee_mortgage_payment = JUBILEE_MORTGAGE
        jubilee_pmi_payment = JUBILEE_PMI
    else:
        jubilee_mortgage_payment = 0
        jubilee_pmi_payment = 0

    # Monthly costs
    jubilee_pretax = (jubilee_mortgage_payment + jubilee_pmi_payment + land_lease_monthly +
                     property_tax_monthly + insurance_monthly + maintenance_monthly)

    # Tax benefit
    months_paid_start = (year - 1) * 12
    jubilee_interest_annual = jubilee_mortgage_balance * JUBILEE_RATE if year <= 30 else 0
    property_tax_annual = property_tax_monthly * 12
    jubilee_tax_benefit = calculate_tax_benefit(jubilee_interest_annual, property_tax_annual)

    jubilee_aftertax = jubilee_pretax - jubilee_tax_benefit

    # No monthly savings (Jubilee is baseline - they spend all their income)
    jubilee_savings = 0

    # Grow portfolio
    for m in range(12):
        jubilee_portfolio = (jubilee_portfolio + jubilee_savings) * (1 + MONTHLY_RETURN)

    # Update mortgage balance
    months_paid_end = year * 12
    jubilee_mortgage_balance = calculate_remaining_balance(JUBILEE_LOAN, JUBILEE_RATE, JUBILEE_MORTGAGE, months_paid_end)

    # Home appreciation
    jubilee_home_value = jubilee_home_value * (1 + HOME_APPRECIATION)

    # Equity
    jubilee_house_value = jubilee_home_value * 0.40
    jubilee_equity = max(0, jubilee_house_value - jubilee_mortgage_balance)

    jubilee_networth = jubilee_portfolio + jubilee_equity

    # ========================================================================
    # SCENARIO B: SAVE & WAIT FOR TRADITIONAL
    # ========================================================================

    if year == 1:
        # Initialize
        wait_portfolio = STARTING_CASH
        wait_bought_yet = False
        wait_mortgage_balance = 0
        wait_home_value = 0
        wait_loan_amount = 0

    # Check if they've bought yet
    if year > wait_years and not wait_bought_yet:
        wait_bought_yet = True
        wait_purchase_year = year
        # They bought at beginning of this year
        wait_home_value = home_price_when_buy
        wait_loan_amount = wait_home_value * 0.80
        wait_mortgage_balance = wait_loan_amount
        wait_portfolio = remaining_portfolio_after_purchase
        wait_mortgage_payment = TRADITIONAL_MORTGAGE_CALC(wait_loan_amount)

    if not wait_bought_yet:
        # Still renting and saving
        rent_monthly = RENT_Y1 * ((1 + RENT_INCREASE) ** (year - 1))
        renters_insurance_monthly = RENTERS_INSURANCE_Y1 * ((1 + INSURANCE_INCREASE) ** (year - 1))
        wait_monthly_cost = rent_monthly + renters_insurance_monthly
        wait_savings = monthly_savings  # Constant savings

        # Grow portfolio
        for m in range(12):
            wait_portfolio = (wait_portfolio + wait_savings) * (1 + MONTHLY_RETURN)

        wait_equity = 0
        wait_networth = wait_portfolio

    else:
        # Owns home (Traditional)
        years_since_purchase = year - wait_purchase_year
        escalation_2pct_purchase = (1 + PROPERTY_TAX_INCREASE) ** years_since_purchase
        escalation_3pct_purchase = (1 + INSURANCE_INCREASE) ** years_since_purchase

        property_tax_monthly_wait = (wait_home_value * 0.0118) * escalation_2pct_purchase / 12
        insurance_monthly_wait = INSURANCE_Y1 * escalation_3pct_purchase
        maintenance_monthly_wait = MAINTENANCE_Y1 * escalation_3pct_purchase

        # Mortgage payment
        years_since_purchase_mortgage = year - wait_purchase_year
        if years_since_purchase_mortgage < 30:
            wait_mortgage_payment_active = wait_mortgage_payment
        else:
            wait_mortgage_payment_active = 0

        # Monthly costs
        wait_pretax = (wait_mortgage_payment_active + property_tax_monthly_wait +
                      insurance_monthly_wait + maintenance_monthly_wait)

        # Tax benefit
        months_paid_since_purchase = years_since_purchase * 12
        remaining_balance_for_interest = calculate_remaining_balance(wait_loan_amount, TRADITIONAL_RATE,
                                                                     wait_mortgage_payment, months_paid_since_purchase)
        deductible_balance = min(remaining_balance_for_interest, MORTGAGE_DEBT_CAP)
        wait_interest_annual = deductible_balance * TRADITIONAL_RATE
        property_tax_annual_wait = property_tax_monthly_wait * 12
        wait_tax_benefit = calculate_tax_benefit(wait_interest_annual, property_tax_annual_wait)

        wait_monthly_cost = wait_pretax - wait_tax_benefit

        # Savings: difference from Jubilee baseline
        wait_savings = jubilee_aftertax - wait_monthly_cost

        # Grow portfolio
        for m in range(12):
            wait_portfolio = (wait_portfolio + wait_savings) * (1 + MONTHLY_RETURN)

        # Update mortgage balance
        months_since_purchase_end = (years_since_purchase + 1) * 12
        wait_mortgage_balance = calculate_remaining_balance(wait_loan_amount, TRADITIONAL_RATE,
                                                            wait_mortgage_payment, months_since_purchase_end)

        # Home appreciation
        wait_home_value = wait_home_value * (1 + HOME_APPRECIATION)

        # Equity
        wait_equity = max(0, wait_home_value - wait_mortgage_balance)

        wait_networth = wait_portfolio + wait_equity

    # Store results
    results.append({
        'year': year,
        'jubilee_networth': jubilee_networth,
        'wait_networth': wait_networth,
        'jubilee_portfolio': jubilee_portfolio,
        'wait_portfolio': wait_portfolio,
        'jubilee_equity': jubilee_equity,
        'wait_equity': wait_equity,
        'wait_bought': wait_bought_yet,
    })

# ============================================================================
# DISPLAY KEY MILESTONES
# ============================================================================

print(f"KEY MILESTONES:")
print("-" * 90)
print()

for yr in [1, int(wait_years), 10, 20, 30]:
    if yr > 30:
        continue
    result = results[yr - 1]
    print(f"YEAR {yr}:")
    if yr == int(wait_years):
        print(f"  (Scenario B buys Traditional this year!)")
    print(f"  Buy Jubilee Now:  ${result['jubilee_networth']:>15,.0f}")
    print(f"  Save & Wait:      ${result['wait_networth']:>15,.0f}")
    diff = result['wait_networth'] - result['jubilee_networth']
    winner = "Save & Wait" if diff > 0 else "Buy Jubilee Now"
    print(f"  Difference:       ${abs(diff):>15,.0f} ({winner})")
    print()

# ============================================================================
# WRITE CSV
# ============================================================================

csv_filename = 'jubilee_now_vs_wait_traditional.csv'
with open(csv_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Year', 'Buy_Jubilee_Now', 'Save_Wait_Traditional'])
    for result in results:
        writer.writerow([
            result['year'],
            int(result['jubilee_networth']),
            int(result['wait_networth'])
        ])

print(f"CSV written to: {csv_filename}")
print()

print("=" * 90)
print("FINAL RESULT (YEAR 30)")
print("=" * 90)
print()

final = results[29]
print(f"Buy Jubilee Now:      ${final['jubilee_networth']:>15,.0f}")
print(f"Save & Wait (Trad):   ${final['wait_networth']:>15,.0f}")
print()

if final['wait_networth'] > final['jubilee_networth']:
    print(f"WINNER: Save & Wait wins by ${final['wait_networth'] - final['jubilee_networth']:,.0f}")
else:
    print(f"WINNER: Buy Jubilee Now wins by ${final['jubilee_networth'] - final['wait_networth']:,.0f}")
print()
