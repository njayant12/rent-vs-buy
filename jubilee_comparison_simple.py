#!/usr/bin/env python3
"""
Jubilee vs 20% Down vs Renting: Initial Net Worth Comparison

For a $1.9M San Francisco home, comparing three scenarios where everyone
starts with the same capital from saving $7,426/mo for 4 years in stocks,
then letting it grow for 1 more year.

Shows: How much each person has invested vs in home equity after purchase.
"""

# ============================================================================
# ASSUMPTIONS
# ============================================================================

HOME_PRICE = 1_900_000

# Everyone starts with same portfolio after saving for 4 years + 1 year growth
MONTHLY_SAVINGS = 7_426
MONTHS_SAVING = 48  # Save for 4 years
STOCK_RETURN = 0.07
CAP_GAINS_TAX_RATE = 0.243  # 15% Fed + 9.3% CA

# Calculate starting portfolio: Save for 4 years, grow for 1 year
monthly_rate = STOCK_RETURN / 12
fv_factor = ((1 + monthly_rate) ** MONTHS_SAVING - 1) / monthly_rate
value_year4 = MONTHLY_SAVINGS * fv_factor
cost_basis = MONTHLY_SAVINGS * MONTHS_SAVING
portfolio_value = value_year4 * (1 + STOCK_RETURN)  # Grow for Year 5
unrealized_gains = portfolio_value - cost_basis

# Jubilee assumptions
LAND_SHARE = 0.60  # Jubilee owns 60% (land)
HOUSE_SHARE = 0.40  # Buyer owns 40% (house)

print("=" * 80)
print("JUBILEE vs 20% DOWN vs RENTING: NET WORTH COMPARISON")
print("$1.9M San Francisco Home")
print("=" * 80)
print()

print("STARTING POSITION (Year 5, before purchase):")
print(f"  Everyone saved ${MONTHLY_SAVINGS:,.0f}/month for 4 years, then let it grow 1 year")
print(f"  Portfolio value: ${portfolio_value:,.0f}")
print(f"  Cost basis:      ${cost_basis:,.0f}")
print(f"  Unrealized gains: ${unrealized_gains:,.0f}")
print()

# ============================================================================
# SCENARIO 1: JUBILEE
# ============================================================================

print("=" * 80)
print("SCENARIO 1: JUBILEE (Ground Lease)")
print("=" * 80)
print()

# Jubilee: Buy 40% of home (house portion) with FHA 3.5% down
house_value = HOME_PRICE * HOUSE_SHARE
jubilee_down = house_value * 0.035
jubilee_closing = 30_000
jubilee_cash_needed = jubilee_down + jubilee_closing

print(f"Home price: ${HOME_PRICE:,.0f}")
print(f"  Land (60%, Jubilee owns): ${HOME_PRICE * LAND_SHARE:,.0f}")
print(f"  House (40%, You own):     ${house_value:,.0f}")
print()
print(f"Cash needed:")
print(f"  Down payment (3.5%):  ${jubilee_down:,.0f}")
print(f"  Closing costs:        ${jubilee_closing:,.0f}")
print(f"  Total:                ${jubilee_cash_needed:,.0f}")
print()

# Sell just enough stock to cover cash needed
# Need to account for cap gains tax on what we sell
# If we sell portion P: proceeds after tax = P * value - P * gains * tax_rate
# We need: P * value - P * gains * tax_rate = cash_needed
# P * (value - gains * tax_rate) = cash_needed
# P = cash_needed / (value - gains * tax_rate)

jubilee_portion_sold = jubilee_cash_needed / (portfolio_value - unrealized_gains * CAP_GAINS_TAX_RATE)
jubilee_sold = jubilee_portion_sold * portfolio_value
jubilee_basis_sold = jubilee_portion_sold * cost_basis
jubilee_gains_sold = jubilee_portion_sold * unrealized_gains
jubilee_tax = jubilee_gains_sold * CAP_GAINS_TAX_RATE
jubilee_proceeds = jubilee_sold - jubilee_tax

jubilee_remaining = (1 - jubilee_portion_sold) * portfolio_value
jubilee_equity = jubilee_down
jubilee_net_worth = jubilee_remaining + jubilee_equity

print(f"Stock sale:")
print(f"  Sell {jubilee_portion_sold*100:.1f}% of portfolio: ${jubilee_sold:,.0f}")
print(f"  Capital gains tax:        ${jubilee_tax:,.0f}")
print(f"  After-tax proceeds:       ${jubilee_proceeds:,.0f}")
print()
print(f"After purchase:")
print(f"  Amount invested (stocks): ${jubilee_remaining:,.0f}")
print(f"  Equity in home:           ${jubilee_equity:,.0f}")
print(f"  Total net worth:          ${jubilee_net_worth:,.0f}")
print()

# ============================================================================
# SCENARIO 2: TRADITIONAL 20% DOWN
# ============================================================================

print("=" * 80)
print("SCENARIO 2: TRADITIONAL 20% DOWN")
print("=" * 80)
print()

traditional_down = HOME_PRICE * 0.20
traditional_closing = 30_000
traditional_cash_needed = traditional_down + traditional_closing

print(f"Home price: ${HOME_PRICE:,.0f}")
print()
print(f"Cash needed:")
print(f"  Down payment (20%):   ${traditional_down:,.0f}")
print(f"  Closing costs:        ${traditional_closing:,.0f}")
print(f"  Total:                ${traditional_cash_needed:,.0f}")
print()

# Sell stock to cover
traditional_portion_sold = traditional_cash_needed / (portfolio_value - unrealized_gains * CAP_GAINS_TAX_RATE)
traditional_sold = traditional_portion_sold * portfolio_value
traditional_basis_sold = traditional_portion_sold * cost_basis
traditional_gains_sold = traditional_portion_sold * unrealized_gains
traditional_tax = traditional_gains_sold * CAP_GAINS_TAX_RATE
traditional_proceeds = traditional_sold - traditional_tax

traditional_remaining = (1 - traditional_portion_sold) * portfolio_value
traditional_equity = traditional_down
traditional_net_worth = traditional_remaining + traditional_equity

print(f"Stock sale:")
print(f"  Sell {traditional_portion_sold*100:.1f}% of portfolio: ${traditional_sold:,.0f}")
print(f"  Capital gains tax:        ${traditional_tax:,.0f}")
print(f"  After-tax proceeds:       ${traditional_proceeds:,.0f}")
print()
print(f"After purchase:")
print(f"  Amount invested (stocks): ${traditional_remaining:,.0f}")
print(f"  Equity in home:           ${traditional_equity:,.0f}")
print(f"  Total net worth:          ${traditional_net_worth:,.0f}")
print()

# ============================================================================
# SCENARIO 3: RENTING
# ============================================================================

print("=" * 80)
print("SCENARIO 3: RENTING")
print("=" * 80)
print()

print(f"Monthly rent: $5,800")
print(f"No purchase - keep entire portfolio invested")
print()

renter_remaining = portfolio_value
renter_equity = 0
renter_net_worth = renter_remaining

print(f"After Year 5:")
print(f"  Amount invested (stocks): ${renter_remaining:,.0f}")
print(f"  Equity in home:           ${renter_equity:,.0f}")
print(f"  Total net worth:          ${renter_net_worth:,.0f}")
print()

# ============================================================================
# COMPARISON TABLE
# ============================================================================

print("=" * 80)
print("COMPARISON TABLE")
print("=" * 80)
print()

print(f"{'Metric':<30} {'Jubilee':>15} {'20% Down':>15} {'Renting':>15}")
print("-" * 80)
print(f"{'Amount Invested':<30} ${jubilee_remaining:>14,.0f} ${traditional_remaining:>14,.0f} ${renter_remaining:>14,.0f}")
print(f"{'Down Payment':<30} ${jubilee_down:>14,.0f} ${traditional_down:>14,.0f} ${0:>14,.0f}")
print(f"{'Equity':<30} ${jubilee_equity:>14,.0f} ${traditional_equity:>14,.0f} ${renter_equity:>14,.0f}")
print(f"{'Capital Gains Tax Paid':<30} ${jubilee_tax:>14,.0f} ${traditional_tax:>14,.0f} ${0:>14,.0f}")
print(f"{'Total Net Worth':<30} ${jubilee_net_worth:>14,.0f} ${traditional_net_worth:>14,.0f} ${renter_net_worth:>14,.0f}")
print()

# ============================================================================
# KEY INSIGHTS
# ============================================================================

print("=" * 80)
print("KEY INSIGHTS")
print("=" * 80)
print()

capital_diff = jubilee_remaining - traditional_remaining
print(f"1. CAPITAL PRESERVATION:")
print(f"   Jubilee keeps ${capital_diff:,.0f} MORE invested than traditional")
print(f"   That's {jubilee_remaining/traditional_remaining:.1f}x more capital working for you")
print()

print(f"2. TAX EFFICIENCY:")
print(f"   Jubilee pays ${jubilee_tax:,.0f} in cap gains tax")
print(f"   Traditional pays ${traditional_tax:,.0f} in cap gains tax")
print(f"   Traditional pays ${traditional_tax - jubilee_tax:,.0f} MORE")
print()

print(f"3. NET WORTH AT PURCHASE:")
print(f"   Renting:     ${renter_net_worth:,.0f} (highest)")
print(f"   Jubilee:     ${jubilee_net_worth:,.0f}")
print(f"   Traditional: ${traditional_net_worth:,.0f} (lowest)")
print()

print(f"4. THE JUBILEE TRADEOFF:")
print(f"   ✓ Only liquidate {jubilee_portion_sold*100:.1f}% of portfolio (vs {traditional_portion_sold*100:.1f}%)")
print(f"   ✓ Keep ${capital_diff:,.0f} more invested")
print(f"   ✗ Only own 40% of property (vs 100%)")
print(f"   ✗ Only get 40% of appreciation")
print(f"   ✗ Pay monthly land lease to Jubilee")
print()

print("Question: Does keeping $370K invested justify owning 40% vs 100%?")
print()
