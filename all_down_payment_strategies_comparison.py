#!/usr/bin/env python3
"""
Comprehensive Down Payment Strategy Comparison

Compares ALL down payment strategies to the baseline "Fresh RSUs" scenario
where money appears right before purchase with no opportunity cost.

Shows the "drag" (extra cost) of each strategy vs the baseline.
"""

print("=" * 110)
print("COMPREHENSIVE DOWN PAYMENT STRATEGY COMPARISON")
print("All strategies compared to baseline: Fresh RSUs (no opportunity cost)")
print("=" * 110)
print()

# All scenarios with their results (from our previous analyses)
# Format: (name, tax_paid, opportunity_cost, total_drag, description)

scenarios = [
    {
        'name': 'Fresh RSUs (BASELINE)',
        'description': 'RSUs vest right before purchase, sell immediately',
        'upfront_cost': 0,
        'upfront_type': 'None',
        'total_drag': 0,
        'gap': 2_234_418,
        'renting_wins_by': 2_234_418,
    },
    {
        'name': 'Lump sum $410K at Y4, grow 1yr, sell',
        'description': 'Had $410K saved at Year 4, let grow 1 year, then sell',
        'upfront_cost': 6_974,
        'upfront_type': 'Capital gains tax',
        'total_drag': 56_605,
        'gap': 2_291_023,
        'renting_wins_by': 2_291_023,
    },
    {
        'name': 'Monthly contributions 4yr, grow 1yr, sell',
        'description': 'Save $7,426/month for 4 years, grow 1 year, sell in Year 5',
        'upfront_cost': 19_984,
        'upfront_type': 'Capital gains tax',
        'total_drag': 162_198,
        'gap': 2_396_616,
        'renting_wins_by': 2_396_616,
    },
    {
        'name': 'HYSA 5 years @ 3%',
        'description': 'Save $6,342/month in HYSA for 5 years',
        'upfront_cost': 44_054,
        'upfront_type': 'Opportunity cost',
        'total_drag': 357_563,
        'gap': 2_591_981,
        'renting_wins_by': 2_591_981,
    },
    {
        'name': 'HYSA 4 years @ 3%',
        'description': 'Had lump sum 4 years ago, kept in HYSA',
        'upfront_cost': 67_496,
        'upfront_type': 'Opportunity cost',
        'total_drag': 547_834,
        'gap': 2_782_252,
        'renting_wins_by': 2_782_252,
    },
]

# Sort by total drag
scenarios_sorted = sorted(scenarios, key=lambda x: x['total_drag'])

print("=" * 110)
print("RANKING: BEST TO WORST DOWN PAYMENT STRATEGIES")
print("=" * 110)
print()
print(f"{'Rank':<6} {'Strategy':<45} {'Upfront Cost':<20} {'30-Year Drag':<20} {'Gap':<20}")
print("-" * 110)

for i, s in enumerate(scenarios_sorted, 1):
    rank_icon = '🥇' if i == 1 else '🥈' if i == 2 else '🥉' if i == 3 else f"{i}."
    print(f"{rank_icon:<6} {s['name']:<45} ${s['upfront_cost']:>18,} ${s['total_drag']:>18,} ${s['gap']:>18,}")

print()
print("=" * 110)
print("DETAILED BREAKDOWN")
print("=" * 110)
print()

for i, s in enumerate(scenarios_sorted, 1):
    print(f"\n{i}. {s['name']}")
    print(f"   {s['description']}")
    print(f"   • Upfront cost: ${s['upfront_cost']:,} ({s['upfront_type']})")
    print(f"   • 30-year drag vs baseline: ${s['total_drag']:,}")
    print(f"   • Final gap: Renting wins by ${s['gap']:,}")
    if s['total_drag'] > 0:
        print(f"   • Drag as % of down payment: {s['total_drag'] / 410_000 * 100:.1f}%")
        print(f"   • Cost per $1 of down payment: ${s['total_drag'] / 410_000:.2f}")

print()
print("=" * 110)
print("KEY COMPARISONS")
print("=" * 110)
print()

baseline = scenarios_sorted[0]
best_realistic = scenarios_sorted[1]
worst = scenarios_sorted[-1]

print("BASELINE (Fresh RSUs):")
print(f"  • The 'impossible' scenario - money appears with no history")
print(f"  • No opportunity cost, no tax, no drag")
print(f"  • Renting wins by ${baseline['gap']:,}")
print()

print("BEST REALISTIC STRATEGY (Lump sum at Y4, grow 1yr):")
print(f"  • Had $410K magically appear at Year 4, let it grow 1 year")
print(f"  • Pay ${best_realistic['upfront_cost']:,} in capital gains tax")
print(f"  • Only ${best_realistic['total_drag']:,} drag (just {best_realistic['total_drag'] / 410_000 * 100:.1f}% of down payment!)")
print(f"  • Nearly as good as baseline!")
print()

print("MOST REALISTIC STRATEGY (Monthly contributions 4yr, grow 1yr):")
realistic = scenarios_sorted[2]
print(f"  • Save ${7_426:,}/month for 4 years, grow 1 year, sell")
print(f"  • Pay ${realistic['upfront_cost']:,} in capital gains tax")
print(f"  • ${realistic['total_drag']:,} drag ({realistic['total_drag'] / 410_000 * 100:.1f}% of down payment)")
print(f"  • Still reasonable!")
print()

print("WORST STRATEGY (HYSA 4 years):")
print(f"  • Being 'conservative' with HYSA")
print(f"  • Lost ${worst['upfront_cost']:,} in opportunity cost")
print(f"  • ${worst['total_drag']:,} drag ({worst['total_drag'] / 410_000 * 100:.1f}% of down payment!)")
print(f"  • {worst['total_drag'] / best_realistic['total_drag']:.1f}x worse than best realistic strategy!")
print()

print("=" * 110)
print("OPPORTUNITY COST vs CAPITAL GAINS TAX")
print("=" * 110)
print()

print("Strategies that pay CAPITAL GAINS TAX:")
for s in scenarios_sorted:
    if 'Capital gains tax' in s['upfront_type']:
        print(f"  • {s['name']:<45} Tax: ${s['upfront_cost']:>8,}  →  Drag: ${s['total_drag']:>10,}")

print()
print("Strategies that incur OPPORTUNITY COST:")
for s in scenarios_sorted:
    if 'Opportunity cost' in s['upfront_type']:
        print(f"  • {s['name']:<45} Lost: ${s['upfront_cost']:>8,}  →  Drag: ${s['total_drag']:>10,}")

print()
print("=" * 110)
print("THE KEY INSIGHT")
print("=" * 110)
print()

# Calculate the multipliers
cap_gains_scenarios = [s for s in scenarios_sorted if 'Capital gains tax' in s['upfront_type']]
opp_cost_scenarios = [s for s in scenarios_sorted if 'Opportunity cost' in s['upfront_type']]

print("CAPITAL GAINS TAX creates less drag than OPPORTUNITY COST:")
print()
print(f"  • Best cap gains strategy: ${best_realistic['upfront_cost']:,} tax → ${best_realistic['total_drag']:,} drag")
print(f"  • Best opp cost strategy: ${opp_cost_scenarios[0]['upfront_cost']:,} lost → ${opp_cost_scenarios[0]['total_drag']:,} drag")
print()
print(f"  Even though opportunity cost is '{opp_cost_scenarios[0]['upfront_cost'] / best_realistic['upfront_cost']:.1f}x larger' upfront,")
print(f"  the final drag is '{opp_cost_scenarios[0]['total_drag'] / best_realistic['total_drag']:.1f}x larger' over 30 years!")
print()

print("Why? Because you can't recover lost time:")
print("  • Capital gains tax: You earned the gains first, then paid tax")
print("  • Opportunity cost: You never earned the gains in the first place")
print()

print("=" * 110)
print("RECOMMENDATION")
print("=" * 110)
print()

print("If you're planning to buy with 20% down ($410K):")
print()
print("✅ BEST: Get an RSU grant that vests right when you need it (impossible to plan)")
print()
print("✅ GOOD: Save monthly in STOCKS, plan for capital gains tax")
print(f"   • Save ${7_426:,}/month for 4 years")
print(f"   • Let grow 1 year, then sell")
print(f"   • Budget ${19_984:,} for capital gains tax")
print(f"   • Total drag: ${162_198:,} (just {162_198 / 410_000 * 100:.1f}% of down payment)")
print()
print("❌ AVOID: Saving 'safely' in HYSA")
print(f"   • Seems safe, but loses ${44_054:,} to ${67_496:,} in opportunity cost")
print(f"   • That compounds to ${357_563:,} to ${547_834:,} in drag")
print(f"   • Up to {547_834 / 162_198:.1f}x worse than stocks strategy!")
print()

print("The counterintuitive truth: Paying tax on gains is better than avoiding gains.")
print()

print("=" * 110)
