#!/usr/bin/env python3
"""
Down Payment Source Analysis: How WHERE your money comes from affects rent vs buy

Scenarios:
1. Fresh RSUs (vesting right before purchase) - no opportunity cost
2. Saved over 4 years in HYSA/T-bills at 3% after-tax
3. Had to sell long-term investments and pay capital gains tax
4. Already had cash invested at 7% (baseline)

Key insight: The "down payment drag" varies from 0% to 7%+ depending on source!
"""

import matplotlib.pyplot as plt
import numpy as np

# Constants
PROPERTY_PRICE = 1_900_000
DOWN_PAYMENT_PCT = 0.20
CLOSING_COSTS = 30_000
INITIAL_RENT = 5_800
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
RENT_INFLATION = 0.03
INSURANCE_INFLATION = 0.03
PROPERTY_TAX_INFLATION = 0.02
TAX_RATE = 0.413
MORTGAGE_RATE = 0.06
YEARS = 30
STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

# Down payment amounts
TOTAL_DOWN_PAYMENT = PROPERTY_PRICE * DOWN_PAYMENT_PCT  # $380K
TOTAL_UPFRONT = TOTAL_DOWN_PAYMENT + CLOSING_COSTS  # $410K

# Capital gains assumptions (for Scenario 3)
LONG_TERM_CAP_GAINS_FEDERAL = 0.15
CA_STATE_TAX_ON_GAINS = 0.093
COMBINED_CAP_GAINS = LONG_TERM_CAP_GAINS_FEDERAL + CA_STATE_TAX_ON_GAINS  # 24.3%

# Assumed W2 income for calculating RSU tax rate
W2_INCOME = 400_000  # Combined household
RSU_TAX_RATE = 0.32 + 0.093 + 0.0765  # Federal + CA + FICA = 48.95%

def calculate_mortgage_payment(loan_amount):
    """Calculate monthly mortgage payment"""
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = 30 * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

def run_scenario(buyer_starting_capital, renter_starting_capital, scenario_name):
    """Run 30-year rent vs buy analysis with given starting capital"""

    # Buyer setup
    loan_amount = PROPERTY_PRICE - TOTAL_DOWN_PAYMENT
    monthly_mortgage = calculate_mortgage_payment(loan_amount)

    buyer_investments = buyer_starting_capital - TOTAL_UPFRONT
    buyer_home_value = PROPERTY_PRICE
    buyer_mortgage_balance = loan_amount

    # Renter setup
    renter_investments = renter_starting_capital

    # Initial costs
    property_tax = PROPERTY_PRICE * 0.01
    home_insurance = 2_400

    # Track yearly values
    yearly_data = {
        'years': [],
        'renter_net_worth': [],
        'buyer_net_worth': []
    }

    for year in range(1, YEARS + 1):
        # Calculate annual mortgage costs
        annual_mortgage = monthly_mortgage * 12

        # Calculate interest paid this year
        year_start_balance = buyer_mortgage_balance
        total_payment = annual_mortgage
        year_interest = 0
        temp_balance = year_start_balance

        for month in range(12):
            month_interest = temp_balance * (MORTGAGE_RATE / 12)
            month_principal = monthly_mortgage - month_interest
            year_interest += month_interest
            temp_balance -= month_principal

        year_principal = total_payment - year_interest
        buyer_mortgage_balance = max(0, buyer_mortgage_balance - year_principal)

        # Tax benefit
        if loan_amount > MORTGAGE_INTEREST_CAP:
            deductible_interest = year_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
        else:
            deductible_interest = year_interest

        salt_deduction = min(property_tax, SALT_CAP)
        itemized = deductible_interest + salt_deduction
        excess = max(0, itemized - STANDARD_DEDUCTION)
        tax_savings = excess * TAX_RATE

        # After-tax costs
        costs_buyer_before_tax = annual_mortgage + property_tax + home_insurance
        costs_buyer_after_tax = costs_buyer_before_tax - tax_savings
        baseline_monthly_income = costs_buyer_after_tax / 12

        # Renter costs
        annual_rent = INITIAL_RENT * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12

        # Monthly savings
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        # Grow investments
        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

            buyer_investments = buyer_investments * (1 + monthly_investment_rate)

        # Home appreciation
        buyer_home_value = buyer_home_value * (1 + HOME_APPRECIATION)

        # Track yearly values
        buyer_equity = buyer_home_value - buyer_mortgage_balance
        buyer_net_worth = buyer_investments + buyer_equity

        yearly_data['years'].append(year)
        yearly_data['renter_net_worth'].append(renter_investments)
        yearly_data['buyer_net_worth'].append(buyer_net_worth)

        # Inflate costs for next year
        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    return {
        'scenario': scenario_name,
        'renter_final': renter_investments,
        'buyer_final': buyer_net_worth,
        'difference': renter_investments - buyer_net_worth,
        'winner': 'Renting' if renter_investments > buyer_net_worth else 'Buying',
        'yearly_data': yearly_data
    }

print("=" * 100)
print("DOWN PAYMENT SOURCE ANALYSIS: Where Your Money Comes From Matters")
print("=" * 100)
print()
print(f"Property: ${PROPERTY_PRICE:,} | Down Payment Needed: ${TOTAL_UPFRONT:,}")
print(f"Assumptions: 3% home appreciation, 7% investment return, $400K W2 income")
print()

# Scenario 1: Fresh RSUs (vesting right before purchase)
print("\n" + "=" * 100)
print("SCENARIO 1: FRESH RSUs (Vesting Right Before Purchase)")
print("=" * 100)
print()
print("Setup:")
print(f"  • RSUs worth ${TOTAL_UPFRONT:,} (pre-tax) vest right before house purchase")
print(f"  • Tax rate on RSUs: {RSU_TAX_RATE*100:.1f}% (income tax)")
print(f"  • Need ${TOTAL_UPFRONT:,} after-tax → Sell ${TOTAL_UPFRONT/(1-RSU_TAX_RATE):,.0f} in RSUs")
print(f"  • Both scenarios start with $0 OTHER savings")
print()
print("Analysis:")
print("  • Buyer: Uses RSUs for down payment, starts with $0 invested")
print("  • Renter: Takes RSU cash, invests all ${:,.0f} after-tax".format(TOTAL_UPFRONT))
print("  • This is the 'cleanest' comparison - no opportunity cost!")
print()

# For RSUs, both start with the after-tax value
scenario1 = run_scenario(
    buyer_starting_capital=TOTAL_UPFRONT,
    renter_starting_capital=TOTAL_UPFRONT,
    scenario_name="Fresh RSUs"
)

print(f"RESULT: {scenario1['winner']} wins by ${abs(scenario1['difference']):,.0f}")
print(f"  Renting: ${scenario1['renter_final']:,.0f}")
print(f"  Buying:  ${scenario1['buyer_final']:,.0f}")
print()

# Scenario 2: Saved over 4 years in HYSA at 3% after-tax
print("\n" + "=" * 100)
print("SCENARIO 2: SAVED IN HYSA/T-BILLS (3% after-tax over 4 years)")
print("=" * 100)
print()

# Calculate how much needed to save to reach $410K after 4 years at 3%
# FV = PV * (1 + r)^t, solving for PV
years_saving = 4
hysa_rate = 0.03
amount_needed_4_years_ago = TOTAL_UPFRONT / ((1 + hysa_rate) ** years_saving)
print(f"Setup:")
print(f"  • Saved ${amount_needed_4_years_ago:,.0f} four years ago")
print(f"  • Grew at 3% after-tax in HYSA/T-bills")
print(f"  • Now have ${TOTAL_UPFRONT:,.0f} for down payment")
print()
print("Analysis:")
print(f"  • Buyer: Uses ${TOTAL_UPFRONT:,.0f} for down payment, starts with $0 invested")
print(f"  • Renter: Keeps ${TOTAL_UPFRONT:,.0f} invested, switches to 7% stocks going forward")
print(f"  • Drag: 4% differential (7% stocks - 3% HYSA)")
print()

scenario2 = run_scenario(
    buyer_starting_capital=TOTAL_UPFRONT,
    renter_starting_capital=TOTAL_UPFRONT,
    scenario_name="HYSA Savings"
)

print(f"RESULT: {scenario2['winner']} wins by ${abs(scenario2['difference']):,.0f}")
print(f"  Renting: ${scenario2['renter_final']:,.0f}")
print(f"  Buying:  ${scenario2['buyer_final']:,.0f}")
print()

# Scenario 3: Had to sell long-term investments (capital gains tax hit)
print("\n" + "=" * 100)
print("SCENARIO 3: SELL LONG-TERM INVESTMENTS (Capital Gains Tax Hit)")
print("=" * 100)
print()

# Assume the investments had 50% gains (bought for $273K, now worth $410K)
original_cost_basis = TOTAL_UPFRONT / 1.5  # 50% gains
capital_gain = TOTAL_UPFRONT - original_cost_basis
capital_gains_tax = capital_gain * COMBINED_CAP_GAINS

print(f"Setup:")
print(f"  • Have ${TOTAL_UPFRONT:,.0f} invested (cost basis: ${original_cost_basis:,.0f})")
print(f"  • Capital gain: ${capital_gain:,.0f}")
print(f"  • Tax on gain: ${capital_gains_tax:,.0f} ({COMBINED_CAP_GAINS*100:.1f}%)")
print(f"  • After-tax from sale: ${TOTAL_UPFRONT - capital_gains_tax:,.0f}")
print()
print("Analysis:")
print(f"  • Buyer: Sells investments, pays ${capital_gains_tax:,.0f} tax, only has ${TOTAL_UPFRONT - capital_gains_tax:,.0f}")
print(f"           Needs to find another ${capital_gains_tax:,.0f} somewhere (or reduce down payment)")
print(f"  • Renter: Keeps ${TOTAL_UPFRONT:,.0f} invested, no tax event, grows at 7%")
print(f"  • Drag: 7% opportunity cost + ${capital_gains_tax:,.0f} tax hit upfront")
print()

# Buyer gets less capital after paying taxes
scenario3 = run_scenario(
    buyer_starting_capital=TOTAL_UPFRONT - capital_gains_tax,  # Buyer loses to taxes
    renter_starting_capital=TOTAL_UPFRONT,  # Renter keeps it all invested
    scenario_name="Sell Investments (w/ cap gains)"
)

print(f"RESULT: {scenario3['winner']} wins by ${abs(scenario3['difference']):,.0f}")
print(f"  Renting: ${scenario3['renter_final']:,.0f}")
print(f"  Buying:  ${scenario3['buyer_final']:,.0f}")
print()
print(f"Note: Buyer started ${capital_gains_tax:,.0f} behind due to capital gains tax")
print()

# Scenario 4: Already had cash invested at 7% (baseline)
print("\n" + "=" * 100)
print("SCENARIO 4: ALREADY HAD CASH INVESTED (Baseline - Full Opportunity Cost)")
print("=" * 100)
print()
print(f"Setup:")
print(f"  • Both have ${TOTAL_UPFRONT:,.0f} invested at 7%")
print()
print("Analysis:")
print(f"  • Buyer: Sells investments for down payment, starts with $0 invested")
print(f"  • Renter: Keeps ${TOTAL_UPFRONT:,.0f} invested at 7%")
print(f"  • Drag: Full 7% opportunity cost")
print()

scenario4 = run_scenario(
    buyer_starting_capital=TOTAL_UPFRONT,  # Buyer uses it all for down payment
    renter_starting_capital=TOTAL_UPFRONT,  # Renter keeps investing
    scenario_name="Had Cash Invested"
)

print(f"RESULT: {scenario4['winner']} wins by ${abs(scenario4['difference']):,.0f}")
print(f"  Renting: ${scenario4['renter_final']:,.0f}")
print(f"  Buying:  ${scenario4['buyer_final']:,.0f}")
print()

# Summary table
print("\n" + "=" * 100)
print("SUMMARY: HOW DOWN PAYMENT SOURCE AFFECTS THE OUTCOME")
print("=" * 100)
print()
print(f"{'Scenario':<45} {'Renting':<20} {'Buying':<20} {'Winner':<15} {'Margin'}")
print("-" * 100)

all_scenarios = [scenario1, scenario2, scenario3, scenario4]

for s in all_scenarios:
    print(f"{s['scenario']:<45} ${s['renter_final']:>18,.0f} ${s['buyer_final']:>18,.0f} {s['winner']:<15} ${abs(s['difference']):>15,.0f}")

print()
print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()

print("1. FRESH RSUs (No Opportunity Cost):")
print(f"   - Gap: ${abs(scenario1['difference']):,.0f}")
print("   - This is the 'cleanest' rent vs buy comparison")
print("   - You wouldn't have had the money otherwise")
print()

print("2. HYSA SAVINGS (4% Differential):")
print(f"   - Gap: ${abs(scenario2['difference']):,.0f} (same as RSUs)")
print("   - Same outcome as RSUs - both start with same capital")
print("   - The 4 years of 3% vs 7% already happened in the past")
print()

print("3. SELL INVESTMENTS (7% + Tax Hit):")
print(f"   - Gap: ${abs(scenario3['difference']):,.0f}")
print(f"   - Buyer started ${capital_gains_tax:,.0f} behind due to taxes")
print("   - This is the WORST scenario for buying")
print(f"   - Extra penalty: ${abs(scenario3['difference']) - abs(scenario1['difference']):,.0f}")
print()

print("4. HAD CASH INVESTED (7% Opportunity Cost):")
print(f"   - Gap: ${abs(scenario4['difference']):,.0f}")
print("   - Same as RSUs/HYSA - starting capital is key")
print("   - The opportunity cost is already baked into the analysis")
print()

print("=" * 100)
print("THE BOTTOM LINE")
print("=" * 100)
print()
print("Down payment source creates a ${:,.0f} swing in outcomes!".format(
    abs(scenario3['difference']) - abs(scenario1['difference'])
))
print()
print("Best case (RSUs/HYSA):     Renting wins by ${:,.0f}".format(abs(scenario1['difference'])))
print("Worst case (Sell stocks):  Renting wins by ${:,.0f}".format(abs(scenario3['difference'])))
print()
print("Why selling investments is worst:")
print(f"  • Pay ${capital_gains_tax:,.0f} in taxes upfront")
print(f"  • That ${capital_gains_tax:,.0f} could have grown to ${capital_gains_tax * (1.07**30):,.0f} over 30 years!")
print()

# Create visualization
print("\n" + "=" * 100)
print("CREATING VISUALIZATION FOR LINKEDIN...")
print("=" * 100)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# Chart 1: Final net worth comparison
scenarios_names = ['Fresh\nRSUs', 'HYSA\nSavings', 'Sell\nInvestments', 'Had Cash\nInvested']
renter_values = [s['renter_final']/1_000_000 for s in all_scenarios]
buyer_values = [s['buyer_final']/1_000_000 for s in all_scenarios]

x = np.arange(len(scenarios_names))
width = 0.35

bars1 = ax1.bar(x - width/2, renter_values, width, label='Renting', color='#2ecc71', alpha=0.8)
bars2 = ax1.bar(x + width/2, buyer_values, width, label='Buying (20% down)', color='#3498db', alpha=0.8)

ax1.set_xlabel('Down Payment Source', fontsize=12, fontweight='bold')
ax1.set_ylabel('Net Worth After 30 Years ($M)', fontsize=12, fontweight='bold')
ax1.set_title('How Down Payment Source Affects Rent vs Buy\n$1.9M SF Home @ 3% Appreciation',
              fontsize=14, fontweight='bold', pad=20)
ax1.set_xticks(x)
ax1.set_xticklabels(scenarios_names, fontsize=10)
ax1.legend(fontsize=11)
ax1.grid(axis='y', alpha=0.3)
ax1.set_ylim(0, 8)

# Add value labels on bars
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.1f}M',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

# Add annotations for gaps
for i, s in enumerate(all_scenarios):
    gap = abs(s['difference']) / 1_000_000
    y_pos = max(renter_values[i], buyer_values[i]) + 0.3
    ax1.text(i, y_pos, f'Gap: ${gap:.1f}M', ha='center', fontsize=9,
             bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Chart 2: Net worth over time for worst vs best scenario
ax2.plot(scenario1['yearly_data']['years'],
         [x/1_000_000 for x in scenario1['yearly_data']['renter_net_worth']],
         label='Renting (Best Case)', color='#27ae60', linewidth=2.5)
ax2.plot(scenario1['yearly_data']['years'],
         [x/1_000_000 for x in scenario1['yearly_data']['buyer_net_worth']],
         label='Buying (Best Case)', color='#2980b9', linewidth=2.5)
ax2.plot(scenario3['yearly_data']['years'],
         [x/1_000_000 for x in scenario3['yearly_data']['renter_net_worth']],
         label='Renting (Worst Case)', color='#27ae60', linewidth=2.5, linestyle='--')
ax2.plot(scenario3['yearly_data']['years'],
         [x/1_000_000 for x in scenario3['yearly_data']['buyer_net_worth']],
         label='Buying (Worst Case)', color='#2980b9', linewidth=2.5, linestyle='--')

ax2.set_xlabel('Years', fontsize=12, fontweight='bold')
ax2.set_ylabel('Net Worth ($M)', fontsize=12, fontweight='bold')
ax2.set_title('Net Worth Trajectory: Best vs Worst Case\n(Fresh RSUs vs Selling Investments)',
              fontsize=14, fontweight='bold', pad=20)
ax2.legend(fontsize=10, loc='upper left')
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/user/rent-vs-buy/down_payment_source_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: down_payment_source_analysis.png")
print()

# Also create a simplified version for mobile/LinkedIn
fig2, ax = plt.subplots(figsize=(10, 8))

x = np.arange(len(scenarios_names))
width = 0.35

bars1 = ax.bar(x - width/2, renter_values, width, label='Renting', color='#2ecc71', alpha=0.8)
bars2 = ax.bar(x + width/2, buyer_values, width, label='Buying (20% down)', color='#3498db', alpha=0.8)

ax.set_xlabel('Down Payment Source', fontsize=14, fontweight='bold')
ax.set_ylabel('Net Worth After 30 Years ($M)', fontsize=14, fontweight='bold')
ax.set_title('Where Your Down Payment Comes From Matters\n$1.9M Bay Area Home @ 3% Appreciation',
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x)
ax.set_xticklabels(scenarios_names, fontsize=12)
ax.legend(fontsize=13, loc='upper left')
ax.grid(axis='y', alpha=0.3)
ax.set_ylim(0, 8)

# Add value labels
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:.1f}M',
                ha='center', va='bottom', fontsize=11, fontweight='bold')

# Add gap annotations with better positioning
gaps = [abs(s['difference']) / 1_000_000 for s in all_scenarios]
for i, gap in enumerate(gaps):
    y_pos = max(renter_values[i], buyer_values[i]) + 0.4
    ax.text(i, y_pos, f'Gap:\n${gap:.1f}M', ha='center', fontsize=10,
            bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7),
            fontweight='bold')

# Add key insight box
insight_text = (
    "Key Insight:\n"
    f"Selling investments costs ${capital_gains_tax/1000:.0f}K in taxes\n"
    f"→ ${(abs(scenario3['difference']) - abs(scenario1['difference']))/1000:.0f}K bigger gap after 30 years!"
)
ax.text(0.98, 0.05, insight_text, transform=ax.transAxes,
        fontsize=11, verticalalignment='bottom', horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))

plt.tight_layout()
plt.savefig('/home/user/rent-vs-buy/down_payment_source_simple.png', dpi=300, bbox_inches='tight')
print("✓ Saved: down_payment_source_simple.png (LinkedIn-optimized)")
print()

print("=" * 100)
print("LINKEDIN POST MATERIAL")
print("=" * 100)
print()

print("Where your down payment comes from matters more than you think.")
print()
print(f"Same $1.9M Bay Area house. Same 3% appreciation. Different outcomes:")
print()
print("📊 Fresh RSUs (vesting):")
print(f"  → Renting wins by ${abs(scenario1['difference'])/1000:.0f}K")
print()
print("📊 Saved in HYSA over 4 years:")
print(f"  → Renting wins by ${abs(scenario2['difference'])/1000:.0f}K (same as RSUs)")
print()
print("📊 Sell long-term investments:")
print(f"  → Pay ${capital_gains_tax/1000:.0f}K in cap gains tax upfront")
print(f"  → Renting wins by ${abs(scenario3['difference'])/1000:.0f}K (${(abs(scenario3['difference']) - abs(scenario1['difference']))/1000:.0f}K worse!)")
print()
print("The difference? That ${:.0f}K tax hit grows to ${:.0f}K over 30 years.".format(
    capital_gains_tax/1000,
    (abs(scenario3['difference']) - abs(scenario1['difference']))/1000
))
print()
print("Down payment source creates a ${:.0f}K swing in outcomes.".format(
    (abs(scenario3['difference']) - abs(scenario1['difference']))/1000
))
print()
print("This is why 'should I buy?' depends on YOUR situation,")
print("not just housing prices and interest rates.")
print()
print("=" * 100)
