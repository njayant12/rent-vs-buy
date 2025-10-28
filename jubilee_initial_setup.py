#!/usr/bin/env python3
"""
Jubilee vs 20% Down vs Renting: Initial Setup Analysis

Compares three scenarios for a $1.9M SF home:
1. Jubilee (ground lease with FHA financing)
2. Traditional 20% down
3. Renting

All scenarios funded the same way:
- Save monthly in stocks for 4 years at 7%
- Let grow for 1 year (Year 5)
- Sell and pay capital gains tax
- Use proceeds for down payment (or keep invested if renting)

Focus: Initial purchase only - how much each person puts down and has left invested
"""

# Constants
HOME_PRICE = 1_900_000
RENT = 5_800  # Monthly rent

# Tax rates
CAP_GAINS_RATE = 0.243  # 15% federal + 9.3% CA
STOCK_RETURN = 0.07

# Jubilee model assumptions (from Sam's conversation)
LAND_SHARE = 0.60  # Jubilee owns 60% (land)
HOUSE_SHARE = 0.40  # Buyer owns 40% (house with FHA)

# FHA parameters
FHA_DOWN_PAYMENT_PCT = 0.035  # 3.5% down
FHA_UPFRONT_PMI_RATE = 0.0175  # 1.75% upfront PMI (added to loan)
FHA_ANNUAL_PMI_RATE = 0.0055  # 0.55% annual PMI (for future monthly calc)

def calculate_monthly_contribution(target, months, annual_return):
    """Calculate monthly contribution needed to reach target"""
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

def calculate_funding_scenario(target_amount):
    """
    Calculate how to fund a target amount by:
    - Saving monthly for 4 years at 7%
    - Growing for 1 year at 7%
    - Selling and paying capital gains tax

    Returns dict with all the details
    """
    # Step 1: Save for 4 years to reach target
    months_saving = 48
    monthly_contribution = calculate_monthly_contribution(target_amount, months_saving, STOCK_RETURN)
    cost_basis = monthly_contribution * months_saving

    # Step 2: Value at end of Year 4 = target
    value_year4 = target_amount

    # Step 3: Grow for Year 5
    value_year5 = value_year4 * (1 + STOCK_RETURN)

    # Step 4: Calculate capital gains and tax
    total_gains = value_year5 - cost_basis
    cap_gains_tax = total_gains * CAP_GAINS_RATE
    after_tax_proceeds = value_year5 - cap_gains_tax

    return {
        'monthly_contribution': monthly_contribution,
        'months_saving': months_saving,
        'total_contributions': cost_basis,
        'cost_basis': cost_basis,
        'value_year4': value_year4,
        'value_year5': value_year5,
        'capital_gains': total_gains,
        'cap_gains_tax': cap_gains_tax,
        'after_tax_proceeds': after_tax_proceeds,
    }

print("=" * 100)
print("JUBILEE vs 20% DOWN vs RENTING: INITIAL SETUP ANALYSIS")
print(f"$1.9M San Francisco Home")
print("=" * 100)
print()

print("=" * 100)
print("SCENARIO 1: JUBILEE (Ground Lease with FHA Financing)")
print("=" * 100)
print()

# Jubilee calculations
jubilee_land_value = HOME_PRICE * LAND_SHARE
jubilee_house_value = HOME_PRICE * HOUSE_SHARE

jubilee_down_payment = jubilee_house_value * FHA_DOWN_PAYMENT_PCT
jubilee_loan_amount = jubilee_house_value - jubilee_down_payment
jubilee_upfront_pmi = jubilee_loan_amount * FHA_UPFRONT_PMI_RATE
jubilee_closing_costs = 15_000  # Estimate for closing costs

# Upfront PMI gets added to the loan, but buyer needs down payment + closing costs upfront
jubilee_cash_needed = jubilee_down_payment + jubilee_closing_costs
jubilee_total_loan = jubilee_loan_amount + jubilee_upfront_pmi

print("Property Split:")
print(f"  • Land (Jubilee owns): 60% = ${jubilee_land_value:,.0f}")
print(f"  • House (Buyer owns): 40% = ${jubilee_house_value:,.0f}")
print()

print("FHA Financing on House Portion:")
print(f"  • House value: ${jubilee_house_value:,.0f}")
print(f"  • FHA 3.5% down payment: ${jubilee_down_payment:,.0f}")
print(f"  • FHA loan amount: ${jubilee_loan_amount:,.0f}")
print(f"  • Upfront PMI (1.75%): ${jubilee_upfront_pmi:,.0f} (added to loan)")
print(f"  • Total loan with PMI: ${jubilee_total_loan:,.0f}")
print()

print("Upfront Cash Needed:")
print(f"  • Down payment: ${jubilee_down_payment:,.0f}")
print(f"  • Closing costs: ${jubilee_closing_costs:,.0f}")
print(f"  • Total cash needed: ${jubilee_cash_needed:,.0f}")
print()

# Calculate funding for Jubilee
jubilee_funding = calculate_funding_scenario(jubilee_cash_needed)

print("Funding Strategy (Save 4yr, Grow 1yr, Sell):")
print(f"  • Monthly savings (4 years): ${jubilee_funding['monthly_contribution']:,.0f}")
print(f"  • Total contributions: ${jubilee_funding['cost_basis']:,.0f}")
print(f"  • Value at Year 4: ${jubilee_funding['value_year4']:,.0f}")
print(f"  • Value at Year 5 (after 7% growth): ${jubilee_funding['value_year5']:,.0f}")
print(f"  • Capital gains: ${jubilee_funding['capital_gains']:,.0f}")
print(f"  • Capital gains tax (24.3%): ${jubilee_funding['cap_gains_tax']:,.0f}")
print(f"  • After-tax proceeds: ${jubilee_funding['after_tax_proceeds']:,.0f}")
print()

print("At Purchase (Year 5):")
print(f"  • Cash for down payment + closing: ${jubilee_cash_needed:,.0f}")
print(f"  • Remaining invested: ${jubilee_funding['after_tax_proceeds'] - jubilee_cash_needed:,.0f}")
print()

print("=" * 100)
print("SCENARIO 2: TRADITIONAL 20% DOWN")
print("=" * 100)
print()

# Traditional 20% down
traditional_down_payment = HOME_PRICE * 0.20
traditional_closing_costs = 30_000  # Standard closing costs
traditional_cash_needed = traditional_down_payment + traditional_closing_costs
traditional_loan_amount = HOME_PRICE - traditional_down_payment

print("Purchase Details:")
print(f"  • Home price: ${HOME_PRICE:,.0f}")
print(f"  • 20% down payment: ${traditional_down_payment:,.0f}")
print(f"  • Closing costs: ${traditional_closing_costs:,.0f}")
print(f"  • Total cash needed: ${traditional_cash_needed:,.0f}")
print(f"  • Loan amount: ${traditional_loan_amount:,.0f}")
print()

# Calculate funding for traditional
traditional_funding = calculate_funding_scenario(traditional_cash_needed)

print("Funding Strategy (Save 4yr, Grow 1yr, Sell):")
print(f"  • Monthly savings (4 years): ${traditional_funding['monthly_contribution']:,.0f}")
print(f"  • Total contributions: ${traditional_funding['cost_basis']:,.0f}")
print(f"  • Value at Year 4: ${traditional_funding['value_year4']:,.0f}")
print(f"  • Value at Year 5 (after 7% growth): ${traditional_funding['value_year5']:,.0f}")
print(f"  • Capital gains: ${traditional_funding['capital_gains']:,.0f}")
print(f"  • Capital gains tax (24.3%): ${traditional_funding['cap_gains_tax']:,.0f}")
print(f"  • After-tax proceeds: ${traditional_funding['after_tax_proceeds']:,.0f}")
print()

print("At Purchase (Year 5):")
print(f"  • Cash for down payment + closing: ${traditional_cash_needed:,.0f}")
print(f"  • Remaining invested: ${traditional_funding['after_tax_proceeds'] - traditional_cash_needed:,.0f}")
print()

print("=" * 100)
print("SCENARIO 3: RENTING")
print("=" * 100)
print()

# Renting - save much less since no down payment needed
# But let's calculate what they'd have if they saved nothing extra (baseline)
# Actually, for fair comparison, let's say renter saves the minimum (for Jubilee scenario)
# to show opportunity cost

print("Rental Details:")
print(f"  • Monthly rent: ${RENT:,.0f}")
print(f"  • No down payment needed")
print()

# Renter could save the same as Jubilee buyer for fair comparison
renter_funding = jubilee_funding  # Same saving rate as Jubilee

print("Funding Strategy (Same as Jubilee for comparison):")
print(f"  • Monthly savings (4 years): ${renter_funding['monthly_contribution']:,.0f}")
print(f"  • Total contributions: ${renter_funding['cost_basis']:,.0f}")
print(f"  • Value at Year 4: ${renter_funding['value_year4']:,.0f}")
print(f"  • Value at Year 5 (after 7% growth): ${renter_funding['value_year5']:,.0f}")
print(f"  • Capital gains: ${renter_funding['capital_gains']:,.0f}")
print(f"  • Capital gains tax (24.3%): ${renter_funding['cap_gains_tax']:,.0f}")
print(f"  • After-tax proceeds: ${renter_funding['after_tax_proceeds']:,.0f}")
print()

print("At Year 5 (No Purchase):")
print(f"  • Cash for down payment: $0 (renting)")
print(f"  • Full amount invested: ${renter_funding['after_tax_proceeds']:,.0f}")
print()

print("=" * 100)
print("SIDE-BY-SIDE COMPARISON: INITIAL SETUP")
print("=" * 100)
print()

print(f"{'Metric':<45} {'Jubilee':<20} {'20% Down':<20} {'Renting':<20}")
print("-" * 105)
print(f"{'Monthly savings (4 years)':<45} ${jubilee_funding['monthly_contribution']:>18,.0f} ${traditional_funding['monthly_contribution']:>18,.0f} ${renter_funding['monthly_contribution']:>18,.0f}")
print(f"{'Total contributions (cost basis)':<45} ${jubilee_funding['cost_basis']:>18,.0f} ${traditional_funding['cost_basis']:>18,.0f} ${renter_funding['cost_basis']:>18,.0f}")
print(f"{'Value at Year 5 (before tax)':<45} ${jubilee_funding['value_year5']:>18,.0f} ${traditional_funding['value_year5']:>18,.0f} ${renter_funding['value_year5']:>18,.0f}")
print(f"{'Capital gains tax paid':<45} ${jubilee_funding['cap_gains_tax']:>18,.0f} ${traditional_funding['cap_gains_tax']:>18,.0f} ${renter_funding['cap_gains_tax']:>18,.0f}")
print(f"{'After-tax proceeds':<45} ${jubilee_funding['after_tax_proceeds']:>18,.0f} ${traditional_funding['after_tax_proceeds']:>18,.0f} ${renter_funding['after_tax_proceeds']:>18,.0f}")
print()
print(f"{'Cash needed for purchase':<45} ${jubilee_cash_needed:>18,.0f} ${traditional_cash_needed:>18,.0f} ${0:>18,.0f}")
print(f"{'Remaining invested at Year 5':<45} ${jubilee_funding['after_tax_proceeds'] - jubilee_cash_needed:>18,.0f} ${traditional_funding['after_tax_proceeds'] - traditional_cash_needed:>18,.0f} ${renter_funding['after_tax_proceeds']:>18,.0f}")
print()

print("=" * 100)
print("KEY INSIGHTS: INITIAL SETUP")
print("=" * 100)
print()

print("1. MONTHLY SAVINGS REQUIRED:")
monthly_diff_jubilee_traditional = traditional_funding['monthly_contribution'] - jubilee_funding['monthly_contribution']
print(f"   • Jubilee: ${jubilee_funding['monthly_contribution']:,.0f}/month (LOWEST)")
print(f"   • 20% Down: ${traditional_funding['monthly_contribution']:,.0f}/month")
print(f"   • Difference: ${monthly_diff_jubilee_traditional:,.0f}/month more for traditional")
print(f"   • Traditional requires {traditional_funding['monthly_contribution'] / jubilee_funding['monthly_contribution']:.2f}x more monthly savings!")
print()

print("2. DOWN PAYMENT COMPARISON:")
down_payment_diff = traditional_cash_needed - jubilee_cash_needed
print(f"   • Jubilee: ${jubilee_cash_needed:,.0f} (3.5% of house portion)")
print(f"   • 20% Down: ${traditional_cash_needed:,.0f} (20% of full price)")
print(f"   • Jubilee saves ${down_payment_diff:,.0f} in upfront cash!")
print()

print("3. CAPITAL AFTER PURCHASE:")
jubilee_remaining = jubilee_funding['after_tax_proceeds'] - jubilee_cash_needed
traditional_remaining = traditional_funding['after_tax_proceeds'] - traditional_cash_needed
renter_remaining = renter_funding['after_tax_proceeds']
print(f"   • Jubilee: ${jubilee_remaining:,.0f} still invested")
print(f"   • 20% Down: ${traditional_remaining:,.0f} still invested")
print(f"   • Renting: ${renter_remaining:,.0f} still invested")
print()
print(f"   Jubilee has ${jubilee_remaining - traditional_remaining:,.0f} MORE invested than traditional buyer!")
print(f"   Renter has ${renter_remaining - jubilee_remaining:,.0f} MORE invested than Jubilee buyer")
print()

print("4. TAX EFFICIENCY:")
print(f"   • Jubilee: Paid ${jubilee_funding['cap_gains_tax']:,.0f} cap gains tax")
print(f"   • 20% Down: Paid ${traditional_funding['cap_gains_tax']:,.0f} cap gains tax")
print(f"   • Renting: Paid ${renter_funding['cap_gains_tax']:,.0f} cap gains tax")
print(f"   • Traditional pays ${traditional_funding['cap_gains_tax'] - jubilee_funding['cap_gains_tax']:,.0f} MORE in tax!")
print()

print("=" * 100)
print("THE JUBILEE ADVANTAGE AT PURCHASE")
print("=" * 100)
print()

print("Jubilee's value proposition:")
print(f"  1. Much lower monthly savings: ${jubilee_funding['monthly_contribution']:,.0f}/mo vs ${traditional_funding['monthly_contribution']:,.0f}/mo")
print(f"  2. Much lower down payment: ${jubilee_cash_needed:,.0f} vs ${traditional_cash_needed:,.0f}")
print(f"  3. More capital invested: ${jubilee_remaining:,.0f} vs ${traditional_remaining:,.0f}")
print()

print("BUT consider:")
print(f"  • You don't own the land (Jubilee owns ${jubilee_land_value:,.0f} worth)")
print(f"  • You pay monthly land lease to Jubilee (TBD)")
print(f"  • You share appreciation based on your ownership % (40% vs 100%)")
print(f"  • You have FHA PMI costs (upfront + annual)")
print()

print("Next step: Calculate monthly costs and 30-year outcomes to see if the upfront")
print("savings justify the ongoing costs and reduced ownership stake.")
print()

print("=" * 100)
