#!/usr/bin/env python3
"""
Down Payment with Year 5 Capital Gains

Scenario:
- Save for 4 years (accumulate cost basis, all becomes long-term)
- Let it grow for 1 more year (year 5)
- Sell at end of year 5, pay capital gains tax ONLY on year 5 growth
- Use proceeds for down payment

This is much better than paying tax on all 4 years of gains!
"""

# Constants
PROPERTY_PRICE = 1_900_000
DOWN_PAYMENT_PCT = 0.20
CLOSING_COSTS = 30_000
TOTAL_UPFRONT = (PROPERTY_PRICE * DOWN_PAYMENT_PCT) + CLOSING_COSTS  # $410K

INVESTMENT_RETURN = 0.07
YEARS = 30

# Capital gains tax (married filing jointly, $400K W2 income in CA)
LONG_TERM_CAP_GAINS_FEDERAL = 0.15  # 15% bracket at $400K income
CA_STATE_TAX_ON_GAINS = 0.093  # CA taxes capital gains as ordinary income
COMBINED_CAP_GAINS = LONG_TERM_CAP_GAINS_FEDERAL + CA_STATE_TAX_ON_GAINS  # 24.3%

print("=" * 100)
print("DOWN PAYMENT SCENARIO: Save Over Years 1-4, Grow in Year 5, Sell and Pay Cap Gains")
print("=" * 100)
print()

# Need $410K after tax
# Cost basis at end of year 4: X
# Grows for 1 year at 7%: X * 1.07
# Pay tax on the gain: (X * 1.07 - X) * 0.243
# After-tax proceeds: X * 1.07 - (X * 1.07 - X) * 0.243 = $410K

# Solve for X:
# X * 1.07 - (X * 0.07) * 0.243 = 410K
# X * 1.07 - X * 0.01701 = 410K
# X * (1.07 - 0.01701) = 410K
# X * 1.05299 = 410K

cost_basis_year4 = TOTAL_UPFRONT / (1.07 - 0.07 * COMBINED_CAP_GAINS)
value_year5 = cost_basis_year4 * 1.07
gain_year5 = value_year5 - cost_basis_year4
capital_gains_tax = gain_year5 * COMBINED_CAP_GAINS
after_tax_proceeds = value_year5 - capital_gains_tax

print("Setup:")
print(f"  • End of Year 4: You have ${cost_basis_year4:,.0f} saved (cost basis)")
print(f"  • End of Year 5: Grew to ${value_year5:,.0f} (at 7%)")
print(f"  • Gain in Year 5: ${gain_year5:,.0f}")
print(f"  • Capital gains tax (24.3%): ${capital_gains_tax:,.0f}")
print(f"  • After-tax proceeds: ${after_tax_proceeds:,.0f}")
print()

print("Comparison:")
print(f"  • Buyer: Sells investments, pays ${capital_gains_tax:,.0f} tax, has ${after_tax_proceeds:,.0f} for down payment")
print(f"  • Renter: Doesn't sell, keeps ${value_year5:,.0f} invested (no tax event)")
print()

# Calculate the drag
# The renter has more capital to start with
renter_advantage = value_year5 - after_tax_proceeds
print(f"Renter starts with ${renter_advantage:,.0f} more capital (the tax that buyer paid)")
print()

# Over 30 years, that compounds to:
compounded_advantage = renter_advantage * ((1 + INVESTMENT_RETURN) ** YEARS)
print(f"That ${renter_advantage:,.0f} compounds to ${compounded_advantage:,.0f} over 30 years")
print()

# Total drag calculation
# This is the "extra gap" compared to if both started with same capital
print("=" * 100)
print("IMPACT ON RENT VS BUY OUTCOME")
print("=" * 100)
print()

# From our previous analysis, we know that with Fresh RSUs (both start with $410K):
# Renting wins by $2.2M

# With this scenario:
# Buyer starts with $410K (after paying tax)
# Renter starts with $417K (doesn't pay tax)
# This creates an extra $6.6K advantage for renter that compounds

baseline_gap = 2_234_418  # From fresh RSUs scenario

# The extra drag is just the compounded tax amount
extra_drag = compounded_advantage - renter_advantage  # The growth on the tax paid

print(f"Baseline scenario (Fresh RSUs, both start with $410K):")
print(f"  Renting wins by ${baseline_gap:,.0f}")
print()

print(f"This scenario (Buyer pays ${capital_gains_tax:,.0f} tax, Renter keeps ${value_year5:,.0f}):")
print(f"  Buyer starts ${renter_advantage:,.0f} behind")
print(f"  That gap compounds to ${compounded_advantage:,.0f} over 30 years")
print(f"  Expected total gap: ~${baseline_gap + compounded_advantage:,.0f}")
print()

# Let's also compare to the other scenarios
print("=" * 100)
print("COMPARISON TO OTHER DOWN PAYMENT STRATEGIES")
print("=" * 100)
print()

print(f"{'Strategy':<50} {'Tax/Cost Upfront':<20} {'30-Year Drag':<20}")
print("-" * 100)
print(f"{'Fresh RSUs (baseline)':<50} ${0:>18,.0f} ${0:>18,.0f}")
print(f"{'Save 4yr in stocks, grow 1yr, sell (THIS)':<50} ${capital_gains_tax:>18,.0f} ${compounded_advantage:>18,.0f}")
print(f"{'Save in HYSA 4 years @ 3%':<50} {'$67K opportunity':>18} ${547_834:>18,.0f}")
print(f"{'Save in stocks 4yr lump sum, sell immediately':<50} ${25_067:>18,.0f} ${203_456:>18,.0f}")
print()

print("=" * 100)
print("KEY INSIGHT")
print("=" * 100)
print()
print(f"By letting your investments grow for one more year BEFORE selling:")
print(f"  • You only pay tax on 1 year of gains (${gain_year5:,.0f})")
print(f"  • Tax owed: ${capital_gains_tax:,.0f} (vs $25,067 in lump sum scenario)")
print(f"  • 30-year drag: ${compounded_advantage:,.0f} (vs $203,456 in lump sum scenario)")
print()
print(f"This is {203_456 / compounded_advantage:.1f}x better than selling everything at once!")
print()
print("However, it still creates ${:,.0f} of drag vs Fresh RSUs.".format(compounded_advantage))
print()

print("=" * 100)
