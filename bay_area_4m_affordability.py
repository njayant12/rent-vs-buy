#!/usr/bin/env python3
"""
Analysis: Can you actually afford a $4M Bay Area home?

Shows the brutal trade-off:
1. High down payment → Massive capital locked up (down payment drag)
2. Low down payment → Insane monthly payments

For each scenario, calculates required post-tax income.
"""

# Constants
PROPERTY_PRICE = 4_000_000
MORTGAGE_RATE = 0.06  # 6% interest rate
YEARS = 30
PROPERTY_TAX_RATE = 0.01  # 1% of purchase price (California)
HOME_INSURANCE_RATE = 0.0012  # 0.12% of home value
PMI_RATE = 0.01  # 1% of purchase price annually (when down payment < 20%)
MAINTENANCE_RATE = 0.01  # 1% of home value annually for maintenance

# Tax rates for high earners in California
FEDERAL_TAX_RATE = 0.32  # 32% federal bracket for high earners
CA_STATE_TAX_RATE = 0.093  # 9.3% California state tax
FICA_RATE = 0.0765  # Social Security + Medicare (capped, but approximate)
COMBINED_TAX_RATE = FEDERAL_TAX_RATE + CA_STATE_TAX_RATE + FICA_RATE

# Deduction constants
STANDARD_DEDUCTION = 31_500  # Married filing jointly
SALT_CAP = 10_000  # SALT deduction cap
MORTGAGE_INTEREST_CAP = 750_000  # Mortgage interest deduction cap (loan amount)

def calculate_monthly_payment(loan_amount):
    """Calculate monthly mortgage payment (principal + interest)"""
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = YEARS * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return monthly_payment

def calculate_scenario(down_payment_pct, scenario_name):
    """Calculate total costs and required income for a given down payment percentage"""

    down_payment = PROPERTY_PRICE * down_payment_pct
    loan_amount = PROPERTY_PRICE - down_payment
    closing_costs = PROPERTY_PRICE * 0.015  # 1.5% closing costs
    total_upfront = down_payment + closing_costs

    # Monthly mortgage payment
    monthly_mortgage = calculate_monthly_payment(loan_amount)
    annual_mortgage = monthly_mortgage * 12

    # Annual costs
    property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE  # $40K/year
    home_insurance = PROPERTY_PRICE * HOME_INSURANCE_RATE  # ~$4.8K/year
    maintenance = PROPERTY_PRICE * MAINTENANCE_RATE  # $40K/year

    # PMI (if down payment < 20%)
    pmi = 0
    if down_payment_pct < 0.20:
        pmi = PROPERTY_PRICE * PMI_RATE

    # Total before-tax costs
    annual_costs_before_tax = annual_mortgage + property_tax + home_insurance + maintenance + pmi

    # Calculate tax benefit (approximate first year)
    # Mortgage interest in year 1 (approximate - most of payment is interest early on)
    year1_interest = loan_amount * MORTGAGE_RATE * 0.95  # ~95% of first year payments are interest

    # Deductible interest (capped at $750K loan)
    if loan_amount > MORTGAGE_INTEREST_CAP:
        deductible_interest = year1_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
    else:
        deductible_interest = year1_interest

    # SALT deduction (property tax capped at $10K)
    salt_deduction = min(property_tax, SALT_CAP)

    # Total itemized deductions
    itemized = deductible_interest + salt_deduction

    # Benefit over standard deduction
    excess = max(0, itemized - STANDARD_DEDUCTION)
    tax_savings = excess * (FEDERAL_TAX_RATE + CA_STATE_TAX_RATE)  # Not FICA

    # After-tax annual costs
    annual_costs_after_tax = annual_costs_before_tax - tax_savings
    monthly_costs_after_tax = annual_costs_after_tax / 12

    # Required income (assuming housing = 40% of take-home pay)
    # This is generous - many lenders want 28-36%
    housing_pct_of_income = 0.40
    required_monthly_income_post_tax = monthly_costs_after_tax / housing_pct_of_income
    required_annual_income_post_tax = required_monthly_income_post_tax * 12

    # Convert to pre-tax income
    # post_tax = pre_tax * (1 - tax_rate)
    # pre_tax = post_tax / (1 - tax_rate)
    required_annual_income_pre_tax = required_annual_income_post_tax / (1 - COMBINED_TAX_RATE)

    # For two W2 workers
    per_person_income = required_annual_income_pre_tax / 2

    return {
        'scenario': scenario_name,
        'down_payment_pct': down_payment_pct * 100,
        'down_payment': down_payment,
        'closing_costs': closing_costs,
        'total_upfront': total_upfront,
        'loan_amount': loan_amount,
        'monthly_mortgage': monthly_mortgage,
        'monthly_property_tax': property_tax / 12,
        'monthly_insurance': home_insurance / 12,
        'monthly_maintenance': maintenance / 12,
        'monthly_pmi': pmi / 12,
        'total_monthly_before_tax': annual_costs_before_tax / 12,
        'tax_savings_monthly': tax_savings / 12,
        'total_monthly_after_tax': monthly_costs_after_tax,
        'required_monthly_income_post_tax': required_monthly_income_post_tax,
        'required_annual_income_post_tax': required_annual_income_post_tax,
        'required_annual_income_pre_tax': required_annual_income_pre_tax,
        'per_person_income': per_person_income,
        'annual_costs_before_tax': annual_costs_before_tax,
        'annual_costs_after_tax': annual_costs_after_tax,
        'tax_savings_annual': tax_savings,
    }

print("=" * 110)
print("CAN YOU ACTUALLY AFFORD A $4M BAY AREA HOME?")
print("The Brutal Math Behind 'Why Don't You Just Buy?'")
print("=" * 110)
print()
print(f"Property Price: ${PROPERTY_PRICE:,}")
print(f"Mortgage Rate: {MORTGAGE_RATE * 100}%")
print(f"Property Tax: {PROPERTY_TAX_RATE * 100}% of purchase price = ${PROPERTY_PRICE * PROPERTY_TAX_RATE:,}/year")
print(f"Maintenance: ~{MAINTENANCE_RATE * 100}% of home value = ${PROPERTY_PRICE * MAINTENANCE_RATE:,}/year")
print()

# Analyze different scenarios
scenarios = [
    (0.03, "SCENARIO 1: Low Down Payment (3%)"),
    (0.20, "SCENARIO 2: Traditional (20% Down)"),
    (0.50, "SCENARIO 3: Half Cash (50% Down)"),
]

results = []

for down_pct, name in scenarios:
    result = calculate_scenario(down_pct, name)
    results.append(result)

    print("=" * 110)
    print(name)
    print("=" * 110)
    print()
    print(f"💰 UPFRONT COSTS:")
    print(f"   Down Payment:     ${result['down_payment']:>15,.0f}  ({result['down_payment_pct']:.0f}%)")
    print(f"   Closing Costs:    ${result['closing_costs']:>15,.0f}")
    print(f"   TOTAL UPFRONT:    ${result['total_upfront']:>15,.0f}")
    print()
    print(f"📊 LOAN DETAILS:")
    print(f"   Loan Amount:      ${result['loan_amount']:>15,.0f}")
    print(f"   Monthly Payment:  ${result['monthly_mortgage']:>15,.0f}")
    print()
    print(f"🏠 MONTHLY COSTS (Year 1):")
    print(f"   Mortgage (P&I):   ${result['monthly_mortgage']:>15,.0f}")
    print(f"   Property Tax:     ${result['monthly_property_tax']:>15,.0f}")
    print(f"   Home Insurance:   ${result['monthly_insurance']:>15,.0f}")
    print(f"   Maintenance:      ${result['monthly_maintenance']:>15,.0f}")
    if result['monthly_pmi'] > 0:
        print(f"   PMI:              ${result['monthly_pmi']:>15,.0f}")
    print(f"                     {'-' * 25}")
    print(f"   Subtotal:         ${result['total_monthly_before_tax']:>15,.0f}")
    print(f"   Tax Savings:     -${result['tax_savings_monthly']:>15,.0f}")
    print(f"   AFTER-TAX COST:   ${result['total_monthly_after_tax']:>15,.0f}")
    print()
    print(f"💵 REQUIRED INCOME (assuming housing = 40% of take-home):")
    print(f"   Monthly Post-Tax: ${result['required_monthly_income_post_tax']:>15,.0f}")
    print(f"   Annual Post-Tax:  ${result['required_annual_income_post_tax']:>15,.0f}")
    print(f"   Annual Pre-Tax:   ${result['required_annual_income_pre_tax']:>15,.0f}")
    print()
    print(f"👥 FOR TWO W2 WORKERS:")
    print(f"   Each person needs: ${result['per_person_income']:>14,.0f}/year")
    print()

# Summary table
print("=" * 110)
print("SUMMARY: THE IMPOSSIBLE CHOICE")
print("=" * 110)
print()
print(f"{'Scenario':<25} {'Upfront $':<20} {'Monthly Cost':<20} {'Income Needed':<25} {'Per Person'}")
print("-" * 110)

for r in results:
    print(f"{r['scenario']:<25} ${r['total_upfront']:>18,.0f} ${r['total_monthly_after_tax']:>18,.0f} ${r['required_annual_income_pre_tax']:>23,.0f} ${r['per_person_income']:>18,.0f}")

print()
print("=" * 110)
print("THE REALITY CHECK")
print("=" * 110)
print()

print("Option 1 (3% Down):")
print(f"  ✗ Need ${results[0]['total_upfront']:,.0f} upfront (might be doable)")
print(f"  ✗ Need ${results[0]['total_monthly_after_tax']:,.0f}/month AFTER TAX")
print(f"  ✗ Requires household pre-tax income: ${results[0]['required_annual_income_pre_tax']:,.0f}")
print(f"  ✗ That's ${results[0]['per_person_income']:,.0f} per person (for two earners)")
print(f"  ✗ Plus paying ${results[0]['monthly_pmi']:,.0f}/month in PMI (dead money)")
print()

print("Option 2 (20% Down):")
print(f"  ✗ Need ${results[1]['total_upfront']:,.0f} upfront (where do you get this??)")
print(f"  ✗ Need ${results[1]['total_monthly_after_tax']:,.0f}/month AFTER TAX")
print(f"  ✗ Requires household pre-tax income: ${results[1]['required_annual_income_pre_tax']:,.0f}")
print(f"  ✗ That's ${results[1]['per_person_income']:,.0f} per person")
print()

print("Option 3 (50% Down):")
print(f"  ✗ Need ${results[2]['total_upfront']:,.0f} upfront (LMAO)")
print(f"  ✗ That's ${results[2]['down_payment']:,.0f} in cash just sitting there")
print(f"  ✗ At 7% investment returns, that's ${results[2]['down_payment'] * 0.07:,.0f}/year in lost gains")
print(f"  ✗ Still need ${results[2]['required_annual_income_pre_tax']:,.0f} household income")
print()

print("=" * 110)
print("WHY 'JUST BUY' ISN'T SIMPLE")
print("=" * 110)
print()

print("The Catch-22:")
print()
print(f"1. If you have ${results[1]['total_upfront']:,.0f} liquid → You're already wealthy")
print(f"   (That's ${results[1]['total_upfront']/30:,.0f} saved per year for 30 years!)")
print()
print(f"2. If you don't have it → You need ${results[0]['required_annual_income_pre_tax']:,.0f} income to qualify")
print(f"   (That's ~${results[0]['per_person_income']:,.0f} each for two FAANG senior engineers)")
print()
print(f"3. If you earn that much → Why tie up ${results[1]['down_payment']:,.0f}?")
print(f"   (Could invest at 7% = ${results[1]['down_payment'] * 0.07:,.0f}/year passive income)")
print()

print("The Real Questions:")
print()
print("• Where do 30-somethings get $860K in cash?")
print("• If you earn $600K/year, why not rent and invest the difference?")
print("• If you inherit $2M, why lock it in a house instead of stocks?")
print()

print("=" * 110)
print("LINKEDIN POST MATERIAL")
print("=" * 110)
print()

print('"Why don\'t you just buy a house?"')
print()
print("Here's why I can't 'just buy' that $4M Bay Area home:")
print()
print("• 3% down: Need $120K upfront + $550K/year income + pay $3,300/month in PMI")
print(f"• 20% down: Need $860K cash upfront (where?) + still need $500K/year income")
print(f"• 50% down: Lock up $2M in a house (losing $140K/year in 7% investment returns)")
print()
print("Pick your poison:")
print("1. Don't have $860K liquid → Can't get traditional mortgage")
print("2. Have $860K liquid → Already wealthy, why lock it up?")
print("3. Stretch with 3% down → Pay $40K/year in PMI + need $550K household income")
print()
print("Every option is brutal. That's the Bay Area housing trap.")
print()

print("=" * 110)
