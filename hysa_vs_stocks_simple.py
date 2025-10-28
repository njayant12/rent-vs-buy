#!/usr/bin/env python3
"""
Simple HYSA vs Stocks Comparison - Verify the Math

Question: To save $410,000 for a down payment over 5 years,
is it better to use HYSA (avoid cap gains tax) or stocks (pay cap gains tax)?
"""

# ============================================================================
# ASSUMPTIONS
# ============================================================================

TARGET = 410_000  # Need $410K for down payment
MONTHS = 60       # Save for 5 years

# HYSA: 4.5% nominal, taxed yearly at 41.3% = 3% after-tax
HYSA_RATE_AFTER_TAX = 0.03

# Stocks: 7% growth, 24.3% cap gains tax when sold
STOCK_RATE = 0.07
CAP_GAINS_TAX_RATE = 0.243

# ============================================================================
# HELPER FUNCTION: Calculate Monthly Contribution
# ============================================================================

def monthly_contribution(target, months, annual_rate):
    """
    How much do you need to save monthly to reach a target?
    Using future value of annuity formula solved for payment.
    """
    monthly_rate = annual_rate / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

# ============================================================================
# HYSA APPROACH
# ============================================================================

print("=" * 70)
print("HYSA APPROACH")
print("=" * 70)

hysa_monthly = monthly_contribution(TARGET, MONTHS, HYSA_RATE_AFTER_TAX)
hysa_total_contrib = hysa_monthly * MONTHS
hysa_final = TARGET
hysa_tax = 0

print(f"Monthly contribution: ${hysa_monthly:,.2f}")
print(f"Total contributed:    ${hysa_total_contrib:,.2f}")
print(f"Final value:          ${hysa_final:,.2f}")
print(f"Tax paid:             ${hysa_tax:,.2f}")
print(f"Available for down:   ${hysa_final:,.2f}")
print()

# ============================================================================
# STOCKS APPROACH
# ============================================================================

print("=" * 70)
print("STOCKS APPROACH")
print("=" * 70)

# Step 1: We need to save enough so that AFTER cap gains tax, we have $410K
# Work backwards: if we need X after tax, and we'll pay Y in tax...
# X = PreTaxValue - (PreTaxValue - CostBasis) * TaxRate
# We need to find PreTaxValue such that X = TARGET

# Iterative approach to find the right target
def find_stock_target(needed_after_tax, months, rate, tax_rate):
    target = needed_after_tax * 1.05  # Initial guess
    for _ in range(10):  # Converge
        monthly = monthly_contribution(target, months, rate)
        cost_basis = monthly * months
        gains = target - cost_basis
        tax = gains * tax_rate
        after_tax = target - tax
        error = needed_after_tax - after_tax
        target += error
    return target, monthly, cost_basis, gains, tax

stock_pretax, stock_monthly, stock_total_contrib, stock_gains, stock_tax = find_stock_target(
    TARGET, MONTHS, STOCK_RATE, CAP_GAINS_TAX_RATE
)

print(f"Monthly contribution: ${stock_monthly:,.2f}")
print(f"Total contributed:    ${stock_total_contrib:,.2f}")
print(f"Value before tax:     ${stock_pretax:,.2f}")
print(f"  - Cost basis:       ${stock_total_contrib:,.2f}")
print(f"  - Capital gains:    ${stock_gains:,.2f}")
print(f"  - Tax (24.3%):      ${stock_tax:,.2f}")
print(f"Available for down:   ${TARGET:,.2f}")
print()

# ============================================================================
# COMPARISON
# ============================================================================

print("=" * 70)
print("COMPARISON")
print("=" * 70)

monthly_diff = hysa_monthly - stock_monthly
contrib_diff = hysa_total_contrib - stock_total_contrib

print(f"HYSA monthly:         ${hysa_monthly:,.2f}")
print(f"Stock monthly:        ${stock_monthly:,.2f}")
print(f"HYSA needs MORE:      ${monthly_diff:,.2f}/month ({monthly_diff/stock_monthly*100:.1f}% more)")
print()
print(f"HYSA total contrib:   ${hysa_total_contrib:,.2f}")
print(f"Stock total contrib:  ${stock_total_contrib:,.2f}")
print(f"HYSA needs MORE:      ${contrib_diff:,.2f} total")
print()
print(f"HYSA tax paid:        ${hysa_tax:,.2f}")
print(f"Stock tax paid:       ${stock_tax:,.2f}")
print()

# ============================================================================
# VERDICT
# ============================================================================

print("=" * 70)
print("VERDICT")
print("=" * 70)
print()
print(f"To avoid ${stock_tax:,.2f} in capital gains tax,")
print(f"you have to contribute ${contrib_diff:,.2f} MORE with HYSA.")
print()
print(f"That's {contrib_diff/stock_tax:.2f}x the tax you're trying to avoid!")
print()
print("Conclusion: Tax avoidance costs more than paying the tax.")
print()
