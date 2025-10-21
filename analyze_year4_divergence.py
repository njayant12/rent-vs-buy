#!/usr/bin/env python3
"""
Analyze why the gap between renting and buying widens at year 4 and beyond
"""

print("="*80)
print("WHY DOES THE GAP WIDEN AT YEAR 4?")
print("="*80)

# Key data from our analysis
year_data = {
    1: {'baseline': 14_028, 'rent_save': 8_054, 'down20_save': 3_520, 'rent_nw': 539_454, 'down20_nw': 499_286},
    2: {'baseline': 14_055, 'rent_save': 7_902, 'down20_save': 3_520, 'rent_nw': 676_373, 'down20_nw': 624_587},
    3: {'baseline': 14_102, 'rent_save': 7_764, 'down20_save': 3_520, 'rent_nw': 821_481, 'down20_nw': 756_253},
    4: {'baseline': 12_566, 'rent_save': 6_038, 'down20_save': 1_937, 'rent_nw': 955_690, 'down20_nw': 875_034},
    5: {'baseline': 12_614, 'rent_save': 5_891, 'down20_save': 1_937, 'rent_nw': 1_097_776, 'down20_nw': 999_531},
    10: {'baseline': 12_872, 'rent_save': 5_077, 'down20_save': 1_937, 'rent_nw': 1_945_419, 'down20_nw': 1_719_658},
    20: {'baseline': 13_456, 'rent_save': 2_980, 'down20_save': 1_937, 'rent_nw': 4_619_910, 'down20_nw': 3_826_657},
    30: {'baseline': 15_098, 'rent_save': 1_020, 'down20_save': 1_937, 'rent_nw': 9_633_324, 'down20_nw': 7_368_324},
}

print("\nYEAR-BY-YEAR MONTHLY INVESTMENT AMOUNTS:")
print(f"{'Year':<6} {'Baseline':<12} {'Rent $':<12} {'20% $':<12} {'Gap':<12} {'Net Worth Gap':<15}")
print("-" * 80)

for year in [1, 2, 3, 4, 5, 10, 20, 30]:
    data = year_data[year]
    gap = data['rent_nw'] - data['down20_nw']
    print(f"{year:<6} ${data['baseline']:>10,} ${data['rent_save']:>10,} ${data['down20_save']:>10,} " +
          f"${data['rent_save'] - data['down20_save']:>10,} ${gap:>13,}")

print("\n" + "="*80)
print("WHAT HAPPENS IN YEAR 4?")
print("="*80)

print("\nYEARS 1-3: PMI Period")
print("-" * 40)
print("3% down pays PMI: $19,000/year")
print("This inflates the baseline income to: ~$14,028/month")
print("\nMonthly investments:")
print("  Renter: $8,054/month")
print("  20% down: $3,520/month")
print("  Difference: $4,534/month advantage for renter")

print("\n\nYEAR 4: PMI REMOVED!")
print("-" * 40)
print("3% down equity reaches 20%")
print("PMI drops to $0")
print("Baseline income drops to: $12,566/month")
print("\nSUDDEN CHANGE in monthly investments:")
print("  Renter: $6,038/month (dropped $2,016!)")
print("  20% down: $1,937/month (dropped $1,583!)")
print("  Difference: $4,101/month")

print("\n\nWHY DOES 20% DOWN DROP MORE?")
print("-" * 40)
print("When baseline drops by $1,462 (from $14,028 to $12,566):")
print("  Renter's costs (rent) are independent - still growing at 3%")
print("  20% down's costs also grow (property tax + insurance)")
print("  But BOTH lose the same baseline income reduction")
print("\nRenter drop: Baseline reduction + rent increase")
print("20% down drop: Baseline reduction affects them more (PMI was in baseline)")

print("\n" + "="*80)
print("WHY DOES THE GAP KEEP GROWING?")
print("="*80)

print("\nTHREE COMPOUNDING EFFECTS:")

print("\n1. EARLY ADVANTAGE COMPOUNDS")
print("   Years 1-3: Renter invests $4,534/month MORE than 20% down")
print("   Total extra: $4,534 × 36 months = $163,224")
print("   This $163K compounds at 7% for the remaining 27 years")
print("   $163K × (1.07^27) = $929,000!")

print("\n2. RENT GROWTH REDUCES RENTER'S ADVANTAGE")
print("   Year 1: Renter saves $8,054/month")
print("   Year 10: Renter saves $5,077/month (rent grew to $7,795/month)")
print("   Year 20: Renter saves $2,980/month (rent grew to $10,476/month)")
print("   Year 30: Renter saves $1,020/month (rent grew to $14,078/month)")
print("   BUT: This is still positive! Renter still invests more than 20% down")

print("\n3. 20% DOWN INVESTMENT STAYS RELATIVELY CONSTANT")
print("   Years 4-30: ~$1,937/month (very stable)")
print("   Their costs grow with property tax (2%) and insurance (3%)")
print("   Baseline grows similarly, so gap stays ~constant")

print("\n" + "="*80)
print("THE DIVERGENCE PATTERN")
print("="*80)

print("\nYears 1-3: Moderate divergence")
print("  - Renter has big advantage ($4,534/month more)")
print("  - But balances are still small, so absolute gap grows slowly")
print("  - Gap grows from $0 to $65K")

print("\nYear 4: INFLECTION POINT")
print("  - PMI drops, baseline crashes")
print("  - Monthly investment amounts reset lower")
print("  - Gap: $65K → $80K")

print("\nYears 5-30: Exponential divergence")
print("  - Early investments compound at 7% for decades")
print("  - Renter's $163K head start from years 1-3 → $929K")
print("  - Renter continues to invest more EVERY year (though decreasing)")
print("  - Gap accelerates: $80K → $225K → $793K → $2.3M")

print("\n" + "="*80)
print("MATHEMATICAL PROOF")
print("="*80)

# Calculate the compound effect
early_advantage = 4_534 * 36  # Months 1-36
years_to_compound = 27
final_value = early_advantage * (1.07 ** years_to_compound)

print(f"\nEarly advantage (Years 1-3):")
print(f"  Extra monthly: $4,534")
print(f"  Total over 36 months: ${early_advantage:,}")
print(f"  Compounds for: {years_to_compound} more years")
print(f"  Final value: ${final_value:,.0f}")

print(f"\nThis alone explains ${final_value:,.0f} of the ${2_265_000:,} gap!")
print(f"That's {(final_value/2_265_000)*100:.1f}% of the total difference!")

print("\n" + "="*80)
print("CONCLUSION")
print("="*80)
print("\nThe gap widens because:")
print("1. Renter invests heavily early (years 1-3) → $929K from compounding")
print("2. Year 4 PMI drop reduces both, but doesn't close the gap")
print("3. Renter continues investing more every year (though advantage shrinks)")
print("4. All advantages compound at 7% for decades")
print("\nThe 'divergence' is exponential compounding in action!")
print("="*80)
