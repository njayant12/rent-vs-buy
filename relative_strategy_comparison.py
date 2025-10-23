#!/usr/bin/env python3
"""
Relative Down Payment Strategy Comparison

Instead of comparing to an "impossible" baseline, compare strategies
to each other to show practical trade-offs.

"If I choose Strategy A instead of Strategy B, what does it cost me?"
"""

print("=" * 100)
print("RELATIVE DOWN PAYMENT STRATEGY COMPARISON")
print("Comparing strategies to each other (not to impossible baseline)")
print("=" * 100)
print()

# All scenarios with their results
scenarios = [
    {
        'name': 'Fresh RSUs',
        'description': 'RSUs vest right before purchase',
        'upfront_cost': 0,
        'gap': 2_234_418,
        'realistic': False,
    },
    {
        'name': 'Lump sum $410K at Y4, grow 1yr',
        'description': '$410K appears at Year 4, grow 1yr, sell',
        'upfront_cost': 6_974,
        'gap': 2_291_023,
        'realistic': False,  # Still requires $410K to magically appear
    },
    {
        'name': 'Monthly stocks 4yr, grow 1yr',
        'description': 'Save $7,426/month in stocks for 4yr',
        'upfront_cost': 19_984,
        'gap': 2_396_616,
        'realistic': True,
    },
    {
        'name': 'HYSA 5 years',
        'description': 'Save $6,342/month in HYSA for 5yr',
        'upfront_cost': 44_054,
        'gap': 2_591_981,
        'realistic': True,
    },
    {
        'name': 'HYSA 4 years',
        'description': 'Lump sum 4yr ago in HYSA',
        'upfront_cost': 67_496,
        'gap': 2_782_252,
        'realistic': False,
    },
]

print("=" * 100)
print("SCENARIO OVERVIEW")
print("=" * 100)
print()
print(f"{'Strategy':<35} {'Upfront Cost':<20} {'Final Gap':<20} {'Realistic?':<15}")
print("-" * 100)
for s in scenarios:
    realistic_mark = '✓' if s['realistic'] else '✗ (requires lump sum)'
    print(f"{s['name']:<35} ${s['upfront_cost']:>18,} ${s['gap']:>18,} {realistic_mark:<15}")

print()
print("=" * 100)
print("PAIRWISE COMPARISONS: 'Choose A instead of B costs you X'")
print("=" * 100)
print()

def compare(scenario_a, scenario_b):
    """Compare two scenarios"""
    difference = scenario_a['gap'] - scenario_b['gap']
    upfront_diff = scenario_a['upfront_cost'] - scenario_b['upfront_cost']

    if difference > 0:
        winner = scenario_b['name']
        loser = scenario_a['name']
        cost = difference
    else:
        winner = scenario_a['name']
        loser = scenario_b['name']
        cost = -difference

    return {
        'better': winner,
        'worse': loser,
        'cost': cost,
        'upfront_diff': upfront_diff,
    }

# Key comparisons
print("1. REALISTIC STRATEGIES: Which actual saving strategy is better?")
print("-" * 100)
print()

monthly_stocks = scenarios[2]
hysa_5yr = scenarios[3]

comp1 = compare(hysa_5yr, monthly_stocks)
print(f"Choosing '{comp1['worse']}' instead of '{comp1['better']}' costs you:")
print(f"  • ${comp1['cost']:,} worse final outcome over 30 years")
print(f"  • Upfront: Pay ${abs(comp1['upfront_diff']):,} less ({'in opportunity cost' if comp1['upfront_diff'] < 0 else 'in tax'})")
print()
print(f"Analysis:")
print(f"  • HYSA: Save ${6_342:,}/month for 5 years, lose ${hysa_5yr['upfront_cost']:,} opportunity cost")
print(f"  • Stocks: Save ${7_426:,}/month for 4 years, pay ${monthly_stocks['upfront_cost']:,} cap gains tax")
print(f"  • Trade-off: Save ${7_426 - 6_342:,}/month less with HYSA, but costs ${comp1['cost']:,} more!")
print()

print("=" * 100)
print()

print("2. BEST REALISTIC vs BASELINE: How much does reality cost?")
print("-" * 100)
print()

fresh_rsu = scenarios[0]
comp2 = compare(monthly_stocks, fresh_rsu)

print(f"Using '{monthly_stocks['name']}' (most realistic) instead of '{fresh_rsu['name']}' (impossible) costs:")
print(f"  • ${comp2['cost']:,} worse outcome")
print(f"  • This is the 'cost of reality' - you have to save over time")
print()

print("=" * 100)
print()

print("3. ALL PAIRWISE COMPARISONS")
print("-" * 100)
print()

# Create comparison matrix
print(f"{'vs':<20}", end='')
for s in scenarios:
    print(f"{s['name'][:20]:<20}", end='')
print()
print("-" * 100)

for i, s1 in enumerate(scenarios):
    print(f"{s1['name'][:20]:<20}", end='')
    for j, s2 in enumerate(scenarios):
        if i == j:
            print(f"{'—':<20}", end='')
        else:
            diff = s1['gap'] - s2['gap']
            if diff > 0:
                print(f"{'+$' + f'{diff:,.0f}':<20}", end='')
            else:
                print(f"{'-$' + f'{abs(diff):,.0f}':<20}", end='')
    print()

print()
print("How to read: Row minus Column = Difference")
print("Positive (+) means row is worse, Negative (-) means row is better")
print()

print("=" * 100)
print("KEY INSIGHTS: THE PRACTICAL TRADE-OFFS")
print("=" * 100)
print()

print("If you're actually planning to save for a down payment:")
print()

print("OPTION 1: Monthly Stocks (4 years)")
print(f"  • Monthly: ${7_426:,}")
print(f"  • Upfront cost: ${monthly_stocks['upfront_cost']:,} in capital gains tax")
print(f"  • Final gap: ${monthly_stocks['gap']:,}")
print()

print("OPTION 2: HYSA (5 years)")
print(f"  • Monthly: ${6_342:,} (${7_426 - 6_342:,}/month less)")
print(f"  • Upfront cost: ${hysa_5yr['upfront_cost']:,} in opportunity cost")
print(f"  • Final gap: ${hysa_5yr['gap']:,}")
print()

print(f"THE TRADE-OFF:")
print(f"  • By choosing HYSA to save ${1_084:,}/month:")
print(f"    - You 'save' ${1_084 * 48:,} in contributions over 4 years")
print(f"    - But you LOSE ${comp1['cost']:,} over 30 years")
print(f"    - That's paying ${comp1['cost'] / (1_084 * 48):.2f} for every $1 you 'saved'!")
print()

print("=" * 100)
print("RECOMMENDATION")
print("=" * 100)
print()

print("Compare strategies based on YOUR situation:")
print()
print("✓ If you can afford ${:,}/month → Choose Monthly Stocks".format(7_426))
print(f"  Best realistic option: ${monthly_stocks['gap']:,} final gap")
print()
print("✗ If you can only afford ${:,}/month → HYSA is worse, consider:".format(6_342))
print(f"  1. Save longer in stocks (5 years at lower monthly amount)")
print(f"  2. Consider 3% down instead (only need ${1_576:,}/month!)")
print(f"  3. Accepting that HYSA costs you ${comp1['cost']:,} more is still buying vs renting")
print()

print("The key question: 'Which saving strategy can I actually execute?'")
print("Then: 'What does that strategy cost me vs alternatives?'")
print()

print("=" * 100)
