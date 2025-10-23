#!/usr/bin/env python3
"""
Down Payment Drag: 3% Down vs 20% Down - Monthly Contributions Scenario

Compares the monthly contribution strategy for both:
- 3% down: Need $87K (much less capital!)
- 20% down: Need $410K

Shows how the lower capital requirement affects the final outcome.
"""

# Constants
PROPERTY_PRICE = 1_900_000
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
PMI_RATE = 0.01  # 1% of purchase price for 3% down

STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

# Capital gains tax
LONG_TERM_CAP_GAINS_FEDERAL = 0.15
CA_STATE_TAX_ON_GAINS = 0.093
COMBINED_CAP_GAINS = LONG_TERM_CAP_GAINS_FEDERAL + CA_STATE_TAX_ON_GAINS

def calculate_mortgage_payment(loan_amount):
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = 30 * 12
    return loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

def calculate_monthly_contribution_needed(target, months, annual_return):
    monthly_rate = annual_return / 12
    fv_factor = ((1 + monthly_rate) ** months - 1) / monthly_rate
    return target / fv_factor

def run_analysis(down_payment_pct, scenario_name):
    """Run full analysis for a given down payment percentage"""

    # Calculate upfront needs
    down_payment = PROPERTY_PRICE * down_payment_pct
    total_upfront = down_payment + CLOSING_COSTS

    # Monthly contribution needed to reach target in 4 years
    months_saving = 48
    monthly_contribution = calculate_monthly_contribution_needed(total_upfront, months_saving, INVESTMENT_RETURN)
    cost_basis = monthly_contribution * months_saving

    # Year 5 growth
    value_end_year5 = total_upfront * (1 + INVESTMENT_RETURN)
    total_gains = value_end_year5 - cost_basis
    capital_gains_tax = total_gains * COMBINED_CAP_GAINS
    after_tax_proceeds = value_end_year5 - capital_gains_tax

    # Setup loan
    loan_amount = PROPERTY_PRICE - down_payment
    monthly_mortgage = calculate_mortgage_payment(loan_amount)

    # Buyer setup
    buyer_investments = after_tax_proceeds - total_upfront
    buyer_home_value = PROPERTY_PRICE
    buyer_mortgage_balance = loan_amount

    # Renter setup (didn't sell, no tax)
    renter_investments = value_end_year5

    # Initial costs
    property_tax = PROPERTY_PRICE * 0.01
    home_insurance = 2_400

    # Track results
    for year in range(1, YEARS + 1):
        # PMI calculation (for 3% down, until 20% equity)
        equity_pct = (buyer_home_value - buyer_mortgage_balance) / PROPERTY_PRICE
        if equity_pct < 0.20:
            annual_pmi = PROPERTY_PRICE * PMI_RATE
        else:
            annual_pmi = 0

        # Mortgage calculations
        annual_mortgage = monthly_mortgage * 12
        year_start_balance = buyer_mortgage_balance
        year_interest = 0
        temp_balance = year_start_balance

        for month in range(12):
            month_interest = temp_balance * (MORTGAGE_RATE / 12)
            month_principal = monthly_mortgage - month_interest
            year_interest += month_interest
            temp_balance -= month_principal

        year_principal = annual_mortgage - year_interest
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
        costs_buyer_before_tax = annual_mortgage + property_tax + home_insurance + annual_pmi
        costs_buyer_after_tax = costs_buyer_before_tax - tax_savings
        baseline_monthly_income = costs_buyer_after_tax / 12

        # Renter costs
        annual_rent = INITIAL_RENT * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        # Grow investments
        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

            buyer_investments = buyer_investments * (1 + monthly_investment_rate)

        # Home appreciation
        buyer_home_value = buyer_home_value * (1 + HOME_APPRECIATION)

        # Inflate costs
        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    # Final positions
    buyer_equity = buyer_home_value - buyer_mortgage_balance
    buyer_net_worth = buyer_investments + buyer_equity
    renter_net_worth = renter_investments

    return {
        'scenario': scenario_name,
        'down_payment_pct': down_payment_pct * 100,
        'total_upfront': total_upfront,
        'monthly_contribution': monthly_contribution,
        'cost_basis': cost_basis,
        'value_year5': value_end_year5,
        'total_gains': total_gains,
        'capital_gains_tax': capital_gains_tax,
        'after_tax_proceeds': after_tax_proceeds,
        'renter_final': renter_net_worth,
        'buyer_final': buyer_net_worth,
        'gap': renter_net_worth - buyer_net_worth
    }

print("=" * 100)
print("DOWN PAYMENT DRAG: 3% Down vs 20% Down - Monthly Contribution Strategy")
print("=" * 100)
print()

# Run both scenarios
scenario_3pct = run_analysis(0.03, "3% Down")
scenario_20pct = run_analysis(0.20, "20% Down")

# Display 3% down results
print("\n" + "=" * 100)
print("SCENARIO 1: 3% DOWN PAYMENT")
print("=" * 100)
print()
print("Saving Phase (Years 1-4):")
print(f"  • Target needed: ${scenario_3pct['total_upfront']:,.0f}")
print(f"  • Monthly contribution: ${scenario_3pct['monthly_contribution']:,.0f}")
print(f"  • Total contributions (cost basis): ${scenario_3pct['cost_basis']:,.0f}")
print(f"  • Portfolio at Year 4: ${scenario_3pct['total_upfront']:,.0f}")
print()
print("Year 5 Growth and Sale:")
print(f"  • Grows to: ${scenario_3pct['value_year5']:,.0f}")
print(f"  • Total capital gain: ${scenario_3pct['total_gains']:,.0f}")
print(f"  • Tax @ 24.3%: ${scenario_3pct['capital_gains_tax']:,.0f}")
print(f"  • After-tax proceeds: ${scenario_3pct['after_tax_proceeds']:,.0f}")
print()
print("30-Year Results:")
print(f"  • Renting: ${scenario_3pct['renter_final']:,.0f}")
print(f"  • Buying (3% down): ${scenario_3pct['buyer_final']:,.0f}")
print(f"  • Gap: ${abs(scenario_3pct['gap']):,.0f} ({'Renting' if scenario_3pct['gap'] > 0 else 'Buying'} wins)")
print()

# Display 20% down results
print("\n" + "=" * 100)
print("SCENARIO 2: 20% DOWN PAYMENT")
print("=" * 100)
print()
print("Saving Phase (Years 1-4):")
print(f"  • Target needed: ${scenario_20pct['total_upfront']:,.0f}")
print(f"  • Monthly contribution: ${scenario_20pct['monthly_contribution']:,.0f}")
print(f"  • Total contributions (cost basis): ${scenario_20pct['cost_basis']:,.0f}")
print(f"  • Portfolio at Year 4: ${scenario_20pct['total_upfront']:,.0f}")
print()
print("Year 5 Growth and Sale:")
print(f"  • Grows to: ${scenario_20pct['value_year5']:,.0f}")
print(f"  • Total capital gain: ${scenario_20pct['total_gains']:,.0f}")
print(f"  • Tax @ 24.3%: ${scenario_20pct['capital_gains_tax']:,.0f}")
print(f"  • After-tax proceeds: ${scenario_20pct['after_tax_proceeds']:,.0f}")
print()
print("30-Year Results:")
print(f"  • Renting: ${scenario_20pct['renter_final']:,.0f}")
print(f"  • Buying (20% down): ${scenario_20pct['buyer_final']:,.0f}")
print(f"  • Gap: ${abs(scenario_20pct['gap']):,.0f} ({'Renting' if scenario_20pct['gap'] > 0 else 'Buying'} wins)")
print()

# Comparison
print("\n" + "=" * 100)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 100)
print()
print(f"{'Metric':<40} {'3% Down':<25} {'20% Down':<25}")
print("-" * 100)
print(f"{'Monthly savings needed (Yrs 1-4)':<40} ${scenario_3pct['monthly_contribution']:>23,.0f} ${scenario_20pct['monthly_contribution']:>23,.0f}")
print(f"{'Total upfront needed':<40} ${scenario_3pct['total_upfront']:>23,.0f} ${scenario_20pct['total_upfront']:>23,.0f}")
print(f"{'Cost basis (contributions)':<40} ${scenario_3pct['cost_basis']:>23,.0f} ${scenario_20pct['cost_basis']:>23,.0f}")
print(f"{'Capital gains tax paid':<40} ${scenario_3pct['capital_gains_tax']:>23,.0f} ${scenario_20pct['capital_gains_tax']:>23,.0f}")
print()
print(f"{'Final net worth (Renting)':<40} ${scenario_3pct['renter_final']:>23,.0f} ${scenario_20pct['renter_final']:>23,.0f}")
print(f"{'Final net worth (Buying)':<40} ${scenario_3pct['buyer_final']:>23,.0f} ${scenario_20pct['buyer_final']:>23,.0f}")
print(f"{'Gap':<40} ${abs(scenario_3pct['gap']):>23,.0f} ${abs(scenario_20pct['gap']):>23,.0f}")
print()

# Key insights
print("\n" + "=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()

print("1. CAPITAL REQUIREMENTS:")
print(f"   • 3% down needs only ${scenario_3pct['monthly_contribution']:,.0f}/month")
print(f"   • 20% down needs ${scenario_20pct['monthly_contribution']:,.0f}/month")
print(f"   • That's {scenario_20pct['monthly_contribution'] / scenario_3pct['monthly_contribution']:.1f}x more for 20% down!")
print()

print("2. CAPITAL GAINS TAX:")
print(f"   • 3% down pays ${scenario_3pct['capital_gains_tax']:,.0f} in tax")
print(f"   • 20% down pays ${scenario_20pct['capital_gains_tax']:,.0f} in tax")
print(f"   • {scenario_20pct['capital_gains_tax'] / scenario_3pct['capital_gains_tax']:.1f}x more tax for 20% down")
print()

print("3. FINAL OUTCOME:")
print(f"   • 3% down: Renting wins by ${abs(scenario_3pct['gap']):,.0f}")
print(f"   • 20% down: Renting wins by ${abs(scenario_20pct['gap']):,.0f}")
print(f"   • 20% down is ${abs(scenario_20pct['gap']) - abs(scenario_3pct['gap']):,.0f} worse!")
print()

print("4. THE TRADE-OFF:")
print(f"   • 3% down: Lower capital needs (${scenario_3pct['total_upfront']:,.0f}), but pay PMI")
print(f"   • 20% down: Higher capital needs (${scenario_20pct['total_upfront']:,.0f}), no PMI")
print(f"   • For rent vs buy: 3% down is ${abs(scenario_20pct['gap']) - abs(scenario_3pct['gap']):,.0f} better")
print(f"     (because you keep ${scenario_20pct['total_upfront'] - scenario_3pct['total_upfront']:,.0f} more invested as renter)")
print()

print("=" * 100)
print("THE BOTTOM LINE")
print("=" * 100)
print()
print("If you're saving monthly over 4 years:")
print()
print(f"3% down strategy:")
print(f"  ✓ Need only ${scenario_3pct['monthly_contribution']:,.0f}/month (achievable)")
print(f"  ✓ Pay only ${scenario_3pct['capital_gains_tax']:,.0f} in capital gains tax")
print(f"  ✗ Pay PMI for a few years")
print(f"  ✓ Better outcome: Renting wins by ${abs(scenario_3pct['gap']):,.0f}")
print()
print(f"20% down strategy:")
print(f"  ✗ Need ${scenario_20pct['monthly_contribution']:,.0f}/month ({scenario_20pct['monthly_contribution'] / scenario_3pct['monthly_contribution']:.1f}x more!)")
print(f"  ✗ Pay ${scenario_20pct['capital_gains_tax']:,.0f} in capital gains tax ({scenario_20pct['capital_gains_tax'] / scenario_3pct['capital_gains_tax']:.1f}x more)")
print(f"  ✓ No PMI")
print(f"  ✗ Worse outcome: Renting wins by ${abs(scenario_20pct['gap']):,.0f}")
print()
print(f"The 20% down payment requirement locks up ${scenario_20pct['total_upfront'] - scenario_3pct['total_upfront']:,.0f} extra capital,")
print(f"which compounds to a ${abs(scenario_20pct['gap']) - abs(scenario_3pct['gap']):,.0f} disadvantage!")
print()
print("=" * 100)
