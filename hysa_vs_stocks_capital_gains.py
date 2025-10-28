#!/usr/bin/env python3
"""
HYSA vs Stocks: Capital Gains Tax is Still Worth It

Comparing saving for down payment in HYSA vs stocks for Jubilee scenarios.

HYSA: 4.5% nominal, taxed yearly at 41.3% = 3.0% after-tax growth
Stocks: 7% growth, taxed only when sold at 24.3%
"""

import math

# Constants
HOME_PRICE = 1_900_000
JUBILEE_CASH_NEEDED = 56_600  # Down payment + closing
TRADITIONAL_CASH_NEEDED = 410_000  # 20% down + closing

# Tax rates
INCOME_TAX_RATE = 0.413  # CA + Federal for high earner
CAP_GAINS_RATE = 0.243   # Federal 15% + CA 9.3%

# Returns
HYSA_NOMINAL = 0.045
HYSA_AFTER_TAX = HYSA_NOMINAL * (1 - INCOME_TAX_RATE)  # 2.64%, round to 3%
HYSA_AFTER_TAX_ROUNDED = 0.03
STOCK_RETURN = 0.07

MONTHS_SAVING = 60  # 5 years

def calculate_monthly_contribution(target, months, annual_return):
    """Calculate monthly contribution needed to reach target"""
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

def calculate_future_value(monthly_contrib, months, annual_return):
    """Calculate future value of monthly contributions"""
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return monthly_contrib * fv_factor

print("=" * 100)
print("HYSA vs STOCKS: IS AVOIDING CAPITAL GAINS TAX WORTH IT?")
print("=" * 100)
print()

print("Scenario: Save for 5 years, then buy")
print()
print("HYSA assumptions:")
print(f"  • Nominal rate: {HYSA_NOMINAL*100:.1f}%")
print(f"  • After-tax rate (taxed yearly at {INCOME_TAX_RATE*100:.1f}%): {HYSA_AFTER_TAX_ROUNDED*100:.1f}%")
print(f"  • No capital gains tax when withdrawing")
print()
print("Stock assumptions:")
print(f"  • Growth rate: {STOCK_RETURN*100:.0f}%")
print(f"  • Capital gains tax only when selling: {CAP_GAINS_RATE*100:.1f}%")
print()

print("=" * 100)
print("SCENARIO 1: JUBILEE (Need $56,600)")
print("=" * 100)
print()

# HYSA approach for Jubilee
hysa_monthly_jubilee = calculate_monthly_contribution(JUBILEE_CASH_NEEDED, MONTHS_SAVING, HYSA_AFTER_TAX_ROUNDED)
hysa_total_contributions_jubilee = hysa_monthly_jubilee * MONTHS_SAVING
hysa_gains_jubilee = JUBILEE_CASH_NEEDED - hysa_total_contributions_jubilee

print("HYSA Approach:")
print(f"  • Monthly savings needed: ${hysa_monthly_jubilee:,.0f}")
print(f"  • Total contributions: ${hysa_total_contributions_jubilee:,.0f}")
print(f"  • Interest earned (already taxed): ${hysa_gains_jubilee:,.0f}")
print(f"  • Final value: ${JUBILEE_CASH_NEEDED:,.0f}")
print(f"  • Capital gains tax: $0")
print(f"  • Cash available: ${JUBILEE_CASH_NEEDED:,.0f}")
print()

# Stocks approach for Jubilee - need to end up with $56,600 AFTER tax
# Work backwards: if final value is V, contributions are C, gains are (V-C)
# After tax = V - (V-C)*0.243 = V - 0.243V + 0.243C = 0.757V + 0.243C
# We need: 0.757V + 0.243C = 56,600
# But C/V ratio depends on the contribution pattern...
# For simplicity: assume ~82% is contributions (based on 5yr at 7%)
# So gains/(value) ≈ 18%, and we need V such that V*0.757 + V*0.82*0.243 = 56,600
# V * (0.757 + 0.199) = V * 0.956 = 56,600, so V = 59,205

# Better approach: iteratively find the target
def find_target_with_tax(needed_after_tax, months, return_rate, tax_rate):
    """Find the target value needed so that after cap gains tax, you have the desired amount"""
    # Start with initial guess
    target = needed_after_tax / 0.82  # rough estimate
    for _ in range(10):  # iterate to converge
        monthly_contrib = calculate_monthly_contribution(target, months, return_rate)
        contributions = monthly_contrib * months
        gains = target - contributions
        tax = gains * tax_rate
        after_tax = target - tax
        # Adjust target
        error = needed_after_tax - after_tax
        target += error
    return target, monthly_contrib, contributions, gains, tax, after_tax

stock_target_jubilee, stock_monthly_jubilee, stock_contributions_jubilee, stock_gains_jubilee, stock_cap_gains_tax_jubilee, stock_after_tax_jubilee = find_target_with_tax(
    JUBILEE_CASH_NEEDED, MONTHS_SAVING, STOCK_RETURN, CAP_GAINS_RATE
)
stock_value_5yr_jubilee = stock_target_jubilee

print("Stock Approach:")
print(f"  • Monthly savings needed: ${stock_monthly_jubilee:,.0f}")
print(f"  • Total contributions: ${stock_contributions_jubilee:,.0f}")
print(f"  • Value after 5 years: ${stock_value_5yr_jubilee:,.0f}")
print(f"  • Capital gains: ${stock_gains_jubilee:,.0f}")
print(f"  • Capital gains tax: ${stock_cap_gains_tax_jubilee:,.0f}")
print(f"  • After-tax proceeds: ${stock_after_tax_jubilee:,.0f}")
print()

print("COMPARISON:")
monthly_diff_jubilee = hysa_monthly_jubilee - stock_monthly_jubilee
total_contrib_diff_jubilee = hysa_total_contributions_jubilee - stock_contributions_jubilee
print(f"  • HYSA requires ${monthly_diff_jubilee:,.0f}/month MORE ({monthly_diff_jubilee/stock_monthly_jubilee*100:.1f}% more)")
print(f"  • HYSA requires ${total_contrib_diff_jubilee:,.0f} MORE total contributions")
print(f"  • Both end with ${JUBILEE_CASH_NEEDED:,.0f} available")
print(f"  • HYSA: Save more ($0 tax) vs Stocks: Save less (pay ${stock_cap_gains_tax_jubilee:,.0f} tax)")
print(f"  • You pay ${total_contrib_diff_jubilee:,.0f} extra to avoid ${stock_cap_gains_tax_jubilee:,.0f} in tax!")
print(f"  • That's paying ${total_contrib_diff_jubilee/stock_cap_gains_tax_jubilee:.2f}x more to avoid the tax!")
print()

print("=" * 100)
print("SCENARIO 2: TRADITIONAL 20% DOWN (Need $410,000)")
print("=" * 100)
print()

# HYSA approach for Traditional
hysa_monthly_traditional = calculate_monthly_contribution(TRADITIONAL_CASH_NEEDED, MONTHS_SAVING, HYSA_AFTER_TAX_ROUNDED)
hysa_total_contributions_traditional = hysa_monthly_traditional * MONTHS_SAVING
hysa_gains_traditional = TRADITIONAL_CASH_NEEDED - hysa_total_contributions_traditional

print("HYSA Approach:")
print(f"  • Monthly savings needed: ${hysa_monthly_traditional:,.0f}")
print(f"  • Total contributions: ${hysa_total_contributions_traditional:,.0f}")
print(f"  • Interest earned (already taxed): ${hysa_gains_traditional:,.0f}")
print(f"  • Final value: ${TRADITIONAL_CASH_NEEDED:,.0f}")
print(f"  • Capital gains tax: $0")
print(f"  • Cash available: ${TRADITIONAL_CASH_NEEDED:,.0f}")
print()

# Stocks approach for Traditional
stock_target_traditional, stock_monthly_traditional, stock_contributions_traditional, stock_gains_traditional, stock_cap_gains_tax_traditional, stock_after_tax_traditional = find_target_with_tax(
    TRADITIONAL_CASH_NEEDED, MONTHS_SAVING, STOCK_RETURN, CAP_GAINS_RATE
)
stock_value_5yr_traditional = stock_target_traditional

print("Stock Approach:")
print(f"  • Monthly savings needed: ${stock_monthly_traditional:,.0f}")
print(f"  • Total contributions: ${stock_contributions_traditional:,.0f}")
print(f"  • Value after 5 years: ${stock_value_5yr_traditional:,.0f}")
print(f"  • Capital gains: ${stock_gains_traditional:,.0f}")
print(f"  • Capital gains tax: ${stock_cap_gains_tax_traditional:,.0f}")
print(f"  • After-tax proceeds: ${stock_after_tax_traditional:,.0f}")
print()

print("COMPARISON:")
monthly_diff_traditional = hysa_monthly_traditional - stock_monthly_traditional
total_contrib_diff_traditional = hysa_total_contributions_traditional - stock_contributions_traditional
print(f"  • HYSA requires ${monthly_diff_traditional:,.0f}/month MORE ({monthly_diff_traditional/stock_monthly_traditional*100:.1f}% more)")
print(f"  • HYSA requires ${total_contrib_diff_traditional:,.0f} MORE total contributions")
print(f"  • Both end with ${TRADITIONAL_CASH_NEEDED:,.0f} available")
print(f"  • HYSA: Save more ($0 tax) vs Stocks: Save less (pay ${stock_cap_gains_tax_traditional:,.0f} tax)")
print(f"  • You pay ${total_contrib_diff_traditional:,.0f} extra to avoid ${stock_cap_gains_tax_traditional:,.0f} in tax!")
print(f"  • That's paying ${total_contrib_diff_traditional/stock_cap_gains_tax_traditional:.2f}x more to avoid the tax!")
print()

print("=" * 100)
print("KEY INSIGHTS: WHY CAPITAL GAINS TAX IS STILL WORTH IT")
print("=" * 100)
print()

print("1. TAX DRAG HURTS MORE THAN TAX PAYMENT:")
print(f"   • HYSA: Taxed EVERY YEAR at {INCOME_TAX_RATE*100:.1f}%")
print(f"   • Stocks: Taxed ONCE at sale at {CAP_GAINS_RATE*100:.1f}%")
print(f"   • Result: {HYSA_AFTER_TAX_ROUNDED*100:.0f}% growth vs {STOCK_RETURN*100:.0f}% growth")
print()

print("2. YOU PAY MORE TO AVOID THE TAX:")
print(f"   • Jubilee: Pay ${total_contrib_diff_jubilee:,.0f} extra to avoid ${stock_cap_gains_tax_jubilee:,.0f} tax = {total_contrib_diff_jubilee/stock_cap_gains_tax_jubilee:.2f}x the tax!")
print(f"   • Traditional: Pay ${total_contrib_diff_traditional:,.0f} extra to avoid ${stock_cap_gains_tax_traditional:,.0f} tax = {total_contrib_diff_traditional/stock_cap_gains_tax_traditional:.2f}x the tax!")
print()

print("3. MONTHLY SAVINGS BURDEN:")
print(f"   • Jubilee: HYSA needs ${monthly_diff_jubilee:,.0f}/mo MORE")
print(f"   • Traditional: HYSA needs ${monthly_diff_traditional:,.0f}/mo MORE")
print()

print("4. TOTAL EXTRA CONTRIBUTIONS:")
print(f"   • Jubilee: HYSA needs ${total_contrib_diff_jubilee:,.0f} MORE out of pocket")
print(f"   • Traditional: HYSA needs ${total_contrib_diff_traditional:,.0f} MORE out of pocket")
print()

print("BOTTOM LINE:")
print(f"")
print(f"To get ${TRADITIONAL_CASH_NEEDED:,.0f} for a traditional down payment:")
print(f"  • HYSA: Save ${hysa_monthly_traditional:,.0f}/month, pay $0 in tax")
print(f"  • Stocks: Save ${stock_monthly_traditional:,.0f}/month, pay ${stock_cap_gains_tax_traditional:,.0f} in tax")
print()
print(f"HYSA saves you ${stock_cap_gains_tax_traditional:,.0f} in taxes...")
print(f"...but costs you ${total_contrib_diff_traditional:,.0f} in extra contributions!")
print()
print(f"That's paying ${total_contrib_diff_traditional/stock_cap_gains_tax_traditional:.2f}x MORE to avoid the tax.")
print()
print("TAX AVOIDANCE IS MORE EXPENSIVE THAN PAYING THE TAX.")
print()
