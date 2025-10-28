#!/usr/bin/env python3
"""
Jubilee vs 20% Down vs Renting: Equal Starting Capital Comparison

Key assumption: Everyone saves $7,426/month for 4 years + grows 1 year
But each scenario only SELLS what they need (minimizing cap gains tax)

This shows the true capital efficiency of each approach.
"""

# Constants
HOME_PRICE = 1_900_000
RENT = 5_800

# Tax rates
CAP_GAINS_RATE = 0.243
STOCK_RETURN = 0.07

# Jubilee assumptions
LAND_SHARE = 0.60
HOUSE_SHARE = 0.40

# Everyone starts with the same portfolio at Year 5
MONTHLY_CONTRIBUTION = 7_426
MONTHS_SAVING = 48
COST_BASIS = MONTHLY_CONTRIBUTION * MONTHS_SAVING  # $356,462
VALUE_YEAR_4 = 410_000  # Target for 20% down
VALUE_YEAR_5 = VALUE_YEAR_4 * (1 + STOCK_RETURN)  # $438,700
TOTAL_GAINS = VALUE_YEAR_5 - COST_BASIS  # $82,238

print("=" * 100)
print("JUBILEE vs 20% DOWN vs RENTING: EQUAL STARTING CAPITAL")
print("Everyone saves $7,426/month for 4 years, grows 1 year")
print("Each scenario only SELLS what they need")
print("=" * 100)
print()

print("STARTING POSITION (Year 5, before any purchase):")
print(f"  • Portfolio value: ${VALUE_YEAR_5:,.0f}")
print(f"  • Cost basis: ${COST_BASIS:,.0f}")
print(f"  • Unrealized gains: ${TOTAL_GAINS:,.0f}")
print()

print("=" * 100)
print("SCENARIO 1: JUBILEE")
print("=" * 100)
print()

# Jubilee cash needs
jubilee_house_value = HOME_PRICE * HOUSE_SHARE
jubilee_down_payment = jubilee_house_value * 0.035
jubilee_closing_costs = 30_000  # SAME as traditional
jubilee_cash_needed = jubilee_down_payment + jubilee_closing_costs

print(f"Cash needed for purchase:")
print(f"  • Down payment (3.5% of ${jubilee_house_value:,.0f}): ${jubilee_down_payment:,.0f}")
print(f"  • Closing costs: ${jubilee_closing_costs:,.0f}")
print(f"  • Total cash needed: ${jubilee_cash_needed:,.0f}")
print()

# Calculate what portion to sell
jubilee_portion_to_sell = jubilee_cash_needed / (VALUE_YEAR_5 - TOTAL_GAINS * CAP_GAINS_RATE)
jubilee_amount_sold = jubilee_portion_to_sell * VALUE_YEAR_5
jubilee_cost_basis_sold = jubilee_portion_to_sell * COST_BASIS
jubilee_gains_on_sale = jubilee_portion_to_sell * TOTAL_GAINS
jubilee_tax_on_sale = jubilee_gains_on_sale * CAP_GAINS_RATE
jubilee_after_tax_proceeds = jubilee_amount_sold - jubilee_tax_on_sale

print(f"Stock sale to fund purchase:")
print(f"  • Sell {jubilee_portion_to_sell*100:.1f}% of portfolio: ${jubilee_amount_sold:,.0f}")
print(f"  • Cost basis of sold portion: ${jubilee_cost_basis_sold:,.0f}")
print(f"  • Capital gains on sale: ${jubilee_gains_on_sale:,.0f}")
print(f"  • Capital gains tax: ${jubilee_tax_on_sale:,.0f}")
print(f"  • After-tax proceeds: ${jubilee_after_tax_proceeds:,.0f}")
print()

# Remaining portfolio
jubilee_remaining_value = (1 - jubilee_portion_to_sell) * VALUE_YEAR_5
jubilee_remaining_basis = (1 - jubilee_portion_to_sell) * COST_BASIS
jubilee_equity = jubilee_down_payment

print(f"Position after purchase:")
print(f"  • Amount still invested: ${jubilee_remaining_value:,.0f}")
print(f"  • Cost basis of investments: ${jubilee_remaining_basis:,.0f}")
print(f"  • Equity in home: ${jubilee_equity:,.0f}")
print(f"  • Capital gains tax paid: ${jubilee_tax_on_sale:,.0f}")
print(f"  • Total net worth: ${jubilee_remaining_value + jubilee_equity:,.0f}")
print()

print("=" * 100)
print("SCENARIO 2: TRADITIONAL 20% DOWN")
print("=" * 100)
print()

# Traditional cash needs
traditional_down_payment = HOME_PRICE * 0.20
traditional_closing_costs = 30_000
traditional_cash_needed = traditional_down_payment + traditional_closing_costs

print(f"Cash needed for purchase:")
print(f"  • Down payment (20%): ${traditional_down_payment:,.0f}")
print(f"  • Closing costs: ${traditional_closing_costs:,.0f}")
print(f"  • Total cash needed: ${traditional_cash_needed:,.0f}")
print()

# Calculate what portion to sell (almost everything)
traditional_portion_to_sell = traditional_cash_needed / (VALUE_YEAR_5 - TOTAL_GAINS * CAP_GAINS_RATE)
traditional_amount_sold = traditional_portion_to_sell * VALUE_YEAR_5
traditional_cost_basis_sold = traditional_portion_to_sell * COST_BASIS
traditional_gains_on_sale = traditional_portion_to_sell * TOTAL_GAINS
traditional_tax_on_sale = traditional_gains_on_sale * CAP_GAINS_RATE
traditional_after_tax_proceeds = traditional_amount_sold - traditional_tax_on_sale

print(f"Stock sale to fund purchase:")
print(f"  • Sell {traditional_portion_to_sell*100:.1f}% of portfolio: ${traditional_amount_sold:,.0f}")
print(f"  • Cost basis of sold portion: ${traditional_cost_basis_sold:,.0f}")
print(f"  • Capital gains on sale: ${traditional_gains_on_sale:,.0f}")
print(f"  • Capital gains tax: ${traditional_tax_on_sale:,.0f}")
print(f"  • After-tax proceeds: ${traditional_after_tax_proceeds:,.0f}")
print()

# Remaining portfolio
traditional_remaining_value = (1 - traditional_portion_to_sell) * VALUE_YEAR_5
traditional_remaining_basis = (1 - traditional_portion_to_sell) * COST_BASIS
traditional_equity = traditional_down_payment

print(f"Position after purchase:")
print(f"  • Amount still invested: ${traditional_remaining_value:,.0f}")
print(f"  • Cost basis of investments: ${traditional_remaining_basis:,.0f}")
print(f"  • Equity in home: ${traditional_equity:,.0f}")
print(f"  • Capital gains tax paid: ${traditional_tax_on_sale:,.0f}")
print(f"  • Total net worth: ${traditional_remaining_value + traditional_equity:,.0f}")
print()

print("=" * 100)
print("SCENARIO 3: RENTING")
print("=" * 100)
print()

print(f"Cash needed for purchase:")
print(f"  • No purchase - continuing to rent at ${RENT:,.0f}/month")
print(f"  • Total cash needed: $0")
print()

print(f"Stock sale to fund purchase:")
print(f"  • Sell 0% of portfolio: $0")
print(f"  • Capital gains tax: $0")
print()

# Full portfolio remains
renter_remaining_value = VALUE_YEAR_5
renter_remaining_basis = COST_BASIS
renter_equity = 0

print(f"Position at Year 5:")
print(f"  • Amount still invested: ${renter_remaining_value:,.0f}")
print(f"  • Cost basis of investments: ${renter_remaining_basis:,.0f}")
print(f"  • Equity in home: ${renter_equity:,.0f}")
print(f"  • Capital gains tax paid: $0")
print(f"  • Total net worth: ${renter_remaining_value:,.0f}")
print()

print("=" * 100)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 100)
print()

print(f"{'Metric':<35} {'Jubilee':<20} {'20% Down':<20} {'Renting':<20}")
print("-" * 95)
print(f"{'Cash needed for purchase':<35} ${jubilee_cash_needed:>18,.0f} ${traditional_cash_needed:>18,.0f} ${0:>18,.0f}")
print(f"{'% of portfolio sold':<35} {jubilee_portion_to_sell*100:>17.1f}% {traditional_portion_to_sell*100:>17.1f}% {0:>17.1f}%")
print(f"{'Capital gains tax paid':<35} ${jubilee_tax_on_sale:>18,.0f} ${traditional_tax_on_sale:>18,.0f} ${0:>18,.0f}")
print()
print(f"{'Amount invested (stocks)':<35} ${jubilee_remaining_value:>18,.0f} ${traditional_remaining_value:>18,.0f} ${renter_remaining_value:>18,.0f}")
print(f"{'Equity in home':<35} ${jubilee_equity:>18,.0f} ${traditional_equity:>18,.0f} ${renter_equity:>18,.0f}")
print(f"{'Total net worth':<35} ${jubilee_remaining_value + jubilee_equity:>18,.0f} ${traditional_remaining_value + traditional_equity:>18,.0f} ${renter_remaining_value:>18,.0f}")
print()

print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()

print("1. TAX EFFICIENCY:")
print(f"   • Jubilee pays ${jubilee_tax_on_sale:,.0f} in cap gains (selling {jubilee_portion_to_sell*100:.1f}%)")
print(f"   • 20% Down pays ${traditional_tax_on_sale:,.0f} in cap gains (selling {traditional_portion_to_sell*100:.1f}%)")
print(f"   • Renting pays $0 (selling 0%)")
print(f"   • Traditional pays ${traditional_tax_on_sale - jubilee_tax_on_sale:,.0f} MORE tax than Jubilee!")
print()

print("2. CAPITAL PRESERVATION:")
capital_diff = jubilee_remaining_value - traditional_remaining_value
print(f"   • Jubilee keeps ${jubilee_remaining_value:,.0f} invested")
print(f"   • 20% Down keeps ${traditional_remaining_value:,.0f} invested")
print(f"   • Jubilee has ${capital_diff:,.0f} MORE invested!")
print(f"   • That's {jubilee_remaining_value / traditional_remaining_value:.1f}x more capital working for you")
print()

print("3. NET WORTH AT PURCHASE:")
nw_diff_jubilee_traditional = (jubilee_remaining_value + jubilee_equity) - (traditional_remaining_value + traditional_equity)
nw_diff_renter_jubilee = renter_remaining_value - (jubilee_remaining_value + jubilee_equity)
print(f"   • Renting: ${renter_remaining_value:,.0f} (highest)")
print(f"   • Jubilee: ${jubilee_remaining_value + jubilee_equity:,.0f}")
print(f"   • 20% Down: ${traditional_remaining_value + traditional_equity:,.0f} (lowest)")
print(f"   • Jubilee beats traditional by ${nw_diff_jubilee_traditional:,.0f}")
print(f"   • Renting beats Jubilee by ${nw_diff_renter_jubilee:,.0f}")
print()

print("4. THE JUBILEE VALUE PROPOSITION:")
print(f"   • Access to homeownership with only {jubilee_portion_to_sell*100:.1f}% portfolio liquidation")
print(f"   • Keep ${capital_diff:,.0f} more capital invested vs traditional")
print(f"   • Pay ${traditional_tax_on_sale - jubilee_tax_on_sale:,.0f} less in taxes upfront")
print(f"   • BUT: Only own 40% of property (vs 100% with traditional)")
print(f"   • BUT: Pay monthly land lease to Jubilee")
print(f"   • BUT: Only get 40% of appreciation")
print()

print("Next: Calculate monthly costs and 30-year outcomes to see if keeping")
print(f"${capital_diff:,.0f} more invested justifies the reduced ownership stake.")
print()
