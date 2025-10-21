#!/usr/bin/env python3
"""
Analyze different home appreciation scenarios:
1. Find break-even appreciation rate (where renting = buying)
2. Show results with 7% appreciation (matching investment return)
"""

# Constants
PROPERTY_PRICE = 1_900_000
DOWN_PAYMENT_PCT = 0.20
CLOSING_COSTS = 30_000
STARTING_CAPITAL = 410_000
INVESTMENT_RETURN = 0.07
INITIAL_RENT = 5_800
RENT_INFLATION = 0.03
INSURANCE_INFLATION = 0.03
PROPERTY_TAX_INFLATION = 0.02  # California Prop 13
TAX_RATE = 0.413
MORTGAGE_RATE = 0.06
YEARS = 30
STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

def calculate_scenario(home_appreciation_rate):
    """Run the full 30-year analysis with given home appreciation rate"""

    # 20% Down Setup
    down_payment = PROPERTY_PRICE * DOWN_PAYMENT_PCT
    loan_amount = PROPERTY_PRICE - down_payment

    # Monthly mortgage payment (principal + interest)
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = YEARS * 12
    monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    # Initial costs
    property_tax = PROPERTY_PRICE * 0.01  # 1% of purchase price
    home_insurance = 2_400  # Annual

    # Starting positions
    buyer_investments = 0
    buyer_home_value = PROPERTY_PRICE
    buyer_mortgage_balance = loan_amount

    renter_investments = STARTING_CAPITAL

    # Track yearly
    for year in range(1, YEARS + 1):
        # Calculate annual costs
        annual_mortgage = monthly_mortgage * 12

        # Calculate mortgage interest for this year (approximate using mid-year balance)
        year_start_balance = buyer_mortgage_balance

        # Calculate how much principal is paid this year
        total_payment = annual_mortgage
        year_interest = 0
        temp_balance = year_start_balance

        for month in range(12):
            month_interest = temp_balance * monthly_rate
            month_principal = monthly_mortgage - month_interest
            year_interest += month_interest
            temp_balance -= month_principal

        year_principal = total_payment - year_interest
        buyer_mortgage_balance -= year_principal

        # Tax benefit calculation
        if loan_amount > MORTGAGE_INTEREST_CAP:
            deductible_interest = year_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
        else:
            deductible_interest = year_interest

        salt_deduction = min(property_tax, SALT_CAP)
        itemized = deductible_interest + salt_deduction
        excess = max(0, itemized - STANDARD_DEDUCTION)
        tax_savings = excess * TAX_RATE

        # After-tax costs
        costs_20_before_tax = annual_mortgage + property_tax + home_insurance
        costs_20_after_tax = costs_20_before_tax - tax_savings

        # This is the baseline - what 20% down spends
        baseline_monthly_income = costs_20_after_tax / 12

        # Renter costs
        annual_rent = INITIAL_RENT * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12

        # Monthly investments
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        # Grow investments (monthly compounding)
        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

        # Home appreciation
        buyer_home_value = buyer_home_value * (1 + home_appreciation_rate)

        # Inflate costs for next year
        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    # Final positions
    buyer_equity = buyer_home_value - buyer_mortgage_balance
    buyer_net_worth = buyer_investments + buyer_equity
    renter_net_worth = renter_investments

    return {
        'renter': renter_net_worth,
        'buyer': buyer_net_worth,
        'buyer_home_value': buyer_home_value,
        'buyer_equity': buyer_equity,
        'difference': renter_net_worth - buyer_net_worth
    }

def find_breakeven_rate():
    """Find the home appreciation rate where renting and buying are equal"""

    print("=" * 90)
    print("FINDING BREAK-EVEN HOME APPRECIATION RATE")
    print("=" * 90)
    print()
    print("Testing different appreciation rates to find where Renting = Buying...")
    print()

    # Test rates from 3% to 15% in 0.1% increments
    best_rate = None
    smallest_diff = float('inf')

    print(f"{'Rate':<8} {'Renter':<15} {'Buyer':<15} {'Difference':<15} {'Winner'}")
    print("-" * 90)

    for rate_pct in range(30, 151, 5):  # 3.0% to 15.0% in 0.5% steps
        rate = rate_pct / 1000
        result = calculate_scenario(rate)

        diff = abs(result['difference'])

        if diff < smallest_diff:
            smallest_diff = diff
            best_rate = rate

        # Print every 0.5%
        winner = "Renting" if result['difference'] > 0 else "Buying"
        print(f"{rate*100:>6.1f}%  ${result['renter']:>13,.0f}  ${result['buyer']:>13,.0f}  ${result['difference']:>13,.0f}  {winner}")

    print()
    print("=" * 90)
    print(f"BREAK-EVEN RATE: {best_rate*100:.1f}% home appreciation")
    print(f"At this rate, difference is only ${smallest_diff:,.0f}")
    print("=" * 90)
    print()

    return best_rate

def analyze_7_percent():
    """Show detailed results with 7% home appreciation"""

    print()
    print("=" * 90)
    print("SCENARIO: 7% HOME APPRECIATION (same as investment return)")
    print("=" * 90)
    print()

    result = calculate_scenario(0.07)

    print("FINAL NET WORTH AFTER 30 YEARS:")
    print(f"  Renting:   ${result['renter']:>13,.0f}")
    print(f"  Buying:    ${result['buyer']:>13,.0f}")
    print()

    if result['difference'] > 0:
        print(f"  Renting wins by ${result['difference']:,.0f}")
    else:
        print(f"  Buying wins by ${-result['difference']:,.0f}")
    print()

    print("BUYING BREAKDOWN:")
    print(f"  Home Value:       ${result['buyer_home_value']:>13,.0f}")
    print(f"  Mortgage Balance: ${0:>13,.0f}  (paid off)")
    print(f"  Home Equity:      ${result['buyer_equity']:>13,.0f}")
    print()

    print("=" * 90)
    print()

if __name__ == "__main__":
    # Find break-even rate
    breakeven = find_breakeven_rate()

    # Analyze 7% scenario
    analyze_7_percent()

    # Quick comparison
    result_3pct = calculate_scenario(0.03)
    result_7pct = calculate_scenario(0.07)
    result_breakeven = calculate_scenario(breakeven)

    print()
    print("=" * 90)
    print("SUMMARY TABLE")
    print("=" * 90)
    print()
    print(f"{'Appreciation':<15} {'Renting':<15} {'Buying':<15} {'Winner':<15} {'Margin'}")
    print("-" * 90)

    scenarios = [
        (0.03, result_3pct),
        (breakeven, result_breakeven),
        (0.07, result_7pct)
    ]

    for rate, result in scenarios:
        winner = "Renting" if result['difference'] > 0 else "Buying"
        margin = abs(result['difference'])
        print(f"{rate*100:>6.1f}%         ${result['renter']:>13,.0f}  ${result['buyer']:>13,.0f}  {winner:<15} ${margin:>13,.0f}")

    print()
    print("=" * 90)
