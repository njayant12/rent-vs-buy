#!/usr/bin/env python3
"""
Detailed Maintenance Cost Calculation
For a $1.9M San Francisco home
"""

# ============================================================================
# BASELINE MAINTENANCE
# ============================================================================
# Regular upkeep: HVAC servicing, minor repairs, landscaping, etc.
BASELINE_ANNUAL = 2_500

# ============================================================================
# MAJOR REPLACEMENTS (Amortized)
# ============================================================================

# Roof replacement
# Typical Bay Area roof: $25K-35K for a standard single-family home
ROOF_COST = 30_000
ROOF_LIFESPAN_YEARS = 30
ROOF_ANNUAL = ROOF_COST / ROOF_LIFESPAN_YEARS

# Flooring replacement
# Assume ~1,800 sq ft at $20/sq ft (hardwood/quality flooring)
# Or ~$30K total for high-quality materials and installation
FLOORING_COST = 30_000
FLOORING_LIFESPAN_YEARS = 10
FLOORING_ANNUAL = FLOORING_COST / FLOORING_LIFESPAN_YEARS

# Interior painting
# Full interior paint for a 3-bed home: $7,500-10,000
PAINTING_COST = 8_000
PAINTING_LIFESPAN_YEARS = 5
PAINTING_ANNUAL = PAINTING_COST / PAINTING_LIFESPAN_YEARS

# ============================================================================
# TOTAL ANNUAL MAINTENANCE
# ============================================================================

TOTAL_ANNUAL = (BASELINE_ANNUAL + ROOF_ANNUAL +
                FLOORING_ANNUAL + PAINTING_ANNUAL)
TOTAL_MONTHLY = TOTAL_ANNUAL / 12

print("=" * 70)
print("DETAILED MAINTENANCE COST BREAKDOWN")
print("=" * 70)
print()

print(f"Baseline maintenance (annual):        ${BASELINE_ANNUAL:>8,.0f}")
print()
print(f"Roof replacement:")
print(f"  Cost: ${ROOF_COST:,.0f} / {ROOF_LIFESPAN_YEARS} years")
print(f"  Amortized annual:                   ${ROOF_ANNUAL:>8,.0f}")
print()
print(f"Flooring replacement:")
print(f"  Cost: ${FLOORING_COST:,.0f} / {FLOORING_LIFESPAN_YEARS} years")
print(f"  Amortized annual:                   ${FLOORING_ANNUAL:>8,.0f}")
print()
print(f"Interior painting:")
print(f"  Cost: ${PAINTING_COST:,.0f} / {PAINTING_LIFESPAN_YEARS} years")
print(f"  Amortized annual:                   ${PAINTING_ANNUAL:>8,.0f}")
print()
print("─" * 70)
print(f"TOTAL ANNUAL MAINTENANCE:             ${TOTAL_ANNUAL:>8,.0f}")
print(f"TOTAL MONTHLY MAINTENANCE:            ${TOTAL_MONTHLY:>8,.0f}")
print()
print(f"As % of home value: {(TOTAL_ANNUAL / 1_900_000) * 100:.2f}%")
print()
print("=" * 70)
print("COMPARISON")
print("=" * 70)
print()
print(f"New maintenance estimate:  ${TOTAL_MONTHLY:>6,.0f}/month")
print(f"Old estimate (1% rule):    ${1_583:>6,.0f}/month")
print(f"Monthly savings:           ${1_583 - TOTAL_MONTHLY:>6,.0f}/month")
print(f"Annual savings:            ${(1_583 - TOTAL_MONTHLY) * 12:>6,.0f}/year")
print()
