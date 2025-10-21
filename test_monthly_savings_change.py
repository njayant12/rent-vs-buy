#!/usr/bin/env python3
"""
Test: Do monthly savings change each year?
"""

PROPERTY_PRICE = 1_900_000
MONTHLY_RENT_Y1 = 5_800
PROPERTY_TAX_Y1 = PROPERTY_PRICE * 0.012
INSURANCE_Y1 = 3_000
MORTGAGE_PI = 11_050  # Fixed
PMI = 1_583  # Fixed (until removed)

print("YEAR-BY-YEAR BASELINE AND SAVINGS CHANGES")
print("="*80)

rent = MONTHLY_RENT_Y1 * 12
prop_tax = PROPERTY_TAX_Y1
insurance = INSURANCE_Y1

for year in range(1, 6):
    # Annual costs
    baseline_annual = (MORTGAGE_PI * 12) + PMI * 12 + prop_tax + insurance
    baseline_monthly = baseline_annual / 12

    rent_monthly = rent / 12

    # For 20% down (no PMI, same mortgage)
    down20_monthly = (9113 * 12 + prop_tax + insurance) / 12

    savings_rent_monthly = baseline_monthly - rent_monthly
    savings_20_monthly = baseline_monthly - down20_monthly

    print(f"\nYear {year}:")
    print(f"  Property tax: ${prop_tax:,.0f}")
    print(f"  Insurance: ${insurance:,.0f}")
    print(f"  Annual rent: ${rent:,.0f}")
    print(f"  Baseline monthly: ${baseline_monthly:,.2f}")
    print(f"  Rent monthly: ${rent_monthly:,.2f}")
    print(f"  20% down monthly: ${down20_monthly:,.2f}")
    print(f"  Renter saves: ${savings_rent_monthly:,.2f}/month = ${savings_rent_monthly*12:,.0f}/year")
    print(f"  20% down saves: ${savings_20_monthly:,.2f}/month = ${savings_20_monthly*12:,.0f}/year")

    # Update for next year
    prop_tax = prop_tax * 1.02
    insurance = insurance * 1.03
    rent = rent * 1.03

print("\n" + "="*80)
print("CONCLUSION: Monthly savings SHOULD change each year!")
print("The code needs to be fixed to recalculate savings annually.")
