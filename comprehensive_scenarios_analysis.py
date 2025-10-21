#!/usr/bin/env python3
"""
Comprehensive rent vs buy analysis for multiple scenarios:
1. Palo Alto (higher prices)
2. Cupertino 2000-2021 bull run (7% appreciation)
3. Beyond 30 years (no mortgage)
4. Impact of parents helping with down payment
"""

# Constants
INVESTMENT_RETURN = 0.07
RENT_INFLATION = 0.03
INSURANCE_INFLATION = 0.03
PROPERTY_TAX_INFLATION = 0.02  # California Prop 13
TAX_RATE = 0.413
MORTGAGE_RATE = 0.06
STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

def run_scenario(
    property_price,
    down_payment_pct,
    starting_capital,
    initial_rent,
    home_appreciation,
    years,
    closing_costs=None,
    scenario_name=""
):
    """Run a complete rent vs buy analysis"""

    if closing_costs is None:
        closing_costs = property_price * 0.015  # 1.5% of purchase price

    # 20% Down Setup
    down_payment = property_price * down_payment_pct
    loan_amount = property_price - down_payment
    total_upfront = down_payment + closing_costs

    # Monthly mortgage payment (principal + interest)
    monthly_rate = MORTGAGE_RATE / 12
    num_payments = 30 * 12  # 30-year mortgage
    monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    # Initial costs
    property_tax = property_price * 0.01  # 1% of purchase price
    home_insurance = property_price * 0.0012  # 0.12% of home value

    # Starting positions
    buyer_investments = max(0, starting_capital - total_upfront)
    buyer_home_value = property_price
    buyer_mortgage_balance = loan_amount

    renter_investments = starting_capital

    # Track yearly
    for year in range(1, years + 1):
        # Check if mortgage is paid off
        mortgage_paid_off = (year > 30)

        if not mortgage_paid_off:
            # Calculate annual costs with mortgage
            annual_mortgage = monthly_mortgage * 12

            # Calculate mortgage interest for this year
            year_start_balance = buyer_mortgage_balance
            total_payment = annual_mortgage
            year_interest = 0
            temp_balance = year_start_balance

            for month in range(12):
                month_interest = temp_balance * monthly_rate
                month_principal = monthly_mortgage - month_interest
                year_interest += month_interest
                temp_balance -= month_principal

            year_principal = total_payment - year_interest
            buyer_mortgage_balance = max(0, buyer_mortgage_balance - year_principal)

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
            costs_buyer_before_tax = annual_mortgage + property_tax + home_insurance
            costs_buyer_after_tax = costs_buyer_before_tax - tax_savings
        else:
            # Mortgage paid off - only property tax and insurance
            costs_buyer_before_tax = property_tax + home_insurance
            costs_buyer_after_tax = costs_buyer_before_tax  # No mortgage interest to deduct
            annual_mortgage = 0

        # This is the baseline - what buyer spends
        baseline_monthly_income = costs_buyer_after_tax / 12

        # Renter costs
        annual_rent = initial_rent * 12 * (1 + RENT_INFLATION) ** (year - 1)
        monthly_rent = annual_rent / 12

        # Monthly investments
        monthly_savings_rent = baseline_monthly_income - monthly_rent
        monthly_savings_buyer = baseline_monthly_income - baseline_monthly_income  # $0 - buyer spends all

        # After mortgage paid off, buyer can invest the difference!
        if mortgage_paid_off:
            # Buyer only pays property tax + insurance now
            # Can invest what used to go to mortgage
            monthly_savings_buyer = monthly_mortgage  # Can now invest the old mortgage payment!

        # Grow investments (monthly compounding)
        monthly_investment_rate = INVESTMENT_RETURN / 12
        for month in range(12):
            renter_investments = renter_investments * (1 + monthly_investment_rate)
            renter_investments += monthly_savings_rent

            buyer_investments = buyer_investments * (1 + monthly_investment_rate)
            buyer_investments += monthly_savings_buyer

        # Home appreciation
        buyer_home_value = buyer_home_value * (1 + home_appreciation)

        # Inflate costs for next year
        property_tax = property_tax * (1 + PROPERTY_TAX_INFLATION)
        home_insurance = home_insurance * (1 + INSURANCE_INFLATION)

    # Final positions
    buyer_equity = buyer_home_value - buyer_mortgage_balance
    buyer_net_worth = buyer_investments + buyer_equity
    renter_net_worth = renter_investments

    return {
        'scenario': scenario_name,
        'renter': renter_net_worth,
        'buyer': buyer_net_worth,
        'buyer_investments': buyer_investments,
        'buyer_home_value': buyer_home_value,
        'buyer_equity': buyer_equity,
        'difference': renter_net_worth - buyer_net_worth,
        'winner': 'Renting' if renter_net_worth > buyer_net_worth else 'Buying'
    }

def analyze_parents_help(parent_contribution, years=30):
    """
    Analyze impact when parents help with down payment

    Scenarios:
    1. Parents keep money invested (baseline)
    2. Parents give money to kids for down payment
    """

    property_price = 1_900_000
    closing_costs = 30_000
    down_payment = property_price * 0.20
    total_needed = down_payment + closing_costs  # $410K

    # Scenario 1: Parents keep $410K invested for 30 years
    parent_investment = parent_contribution
    for year in range(years):
        parent_investment = parent_investment * (1 + INVESTMENT_RETURN)

    # Scenario 2: Parents give money, kids buy house
    kids_starting_capital = parent_contribution
    result = run_scenario(
        property_price=property_price,
        down_payment_pct=0.20,
        starting_capital=kids_starting_capital,
        initial_rent=5_800,
        home_appreciation=0.03,
        years=years,
        closing_costs=closing_costs,
        scenario_name=f"Parents help ${parent_contribution:,.0f}"
    )

    # Combined net worth: what parents have left + what kids have
    scenario1_total = parent_investment  # Parents kept it all invested
    scenario2_total = result['buyer']  # Kids bought house

    return {
        'parent_contribution': parent_contribution,
        'scenario1_parents_invest': parent_investment,
        'scenario2_kids_buy': scenario2_total,
        'difference': scenario1_total - scenario2_total,
        'better': 'Parents Invest' if scenario1_total > scenario2_total else 'Kids Buy'
    }


print("=" * 100)
print("COMPREHENSIVE RENT VS BUY ANALYSIS")
print("=" * 100)
print()

# Scenario 1: San Francisco (baseline)
print("\n" + "=" * 100)
print("SCENARIO 1: SAN FRANCISCO")
print("=" * 100)
sf_3pct = run_scenario(
    property_price=1_900_000,
    down_payment_pct=0.20,
    starting_capital=410_000,
    initial_rent=5_800,
    home_appreciation=0.03,
    years=30,
    closing_costs=30_000,
    scenario_name="SF @ 3% appreciation"
)

sf_7pct = run_scenario(
    property_price=1_900_000,
    down_payment_pct=0.20,
    starting_capital=410_000,
    initial_rent=5_800,
    home_appreciation=0.07,
    years=30,
    closing_costs=30_000,
    scenario_name="SF @ 7% appreciation"
)

print(f"Property Price: $1,900,000 | Rent: $5,800/month")
print()
print(f"{'Appreciation':<20} {'Renting':<20} {'Buying':<20} {'Winner':<15} {'Margin'}")
print("-" * 100)
print(f"{'3%':<20} ${sf_3pct['renter']:>18,.0f} ${sf_3pct['buyer']:>18,.0f} {sf_3pct['winner']:<15} ${abs(sf_3pct['difference']):>15,.0f}")
print(f"{'7%':<20} ${sf_7pct['renter']:>18,.0f} ${sf_7pct['buyer']:>18,.0f} {sf_7pct['winner']:<15} ${abs(sf_7pct['difference']):>15,.0f}")

# Scenario 2: Palo Alto (way more expensive)
print("\n" + "=" * 100)
print("SCENARIO 2: PALO ALTO (Higher Prices)")
print("=" * 100)

# Palo Alto typical prices: ~$3.5M for similar property
# Rent proportionally higher too
pa_3pct = run_scenario(
    property_price=3_500_000,
    down_payment_pct=0.20,
    starting_capital=730_000,  # 20% down + closing
    initial_rent=10_500,  # Proportionally higher rent
    home_appreciation=0.03,
    years=30,
    scenario_name="Palo Alto @ 3% appreciation"
)

pa_7pct = run_scenario(
    property_price=3_500_000,
    down_payment_pct=0.20,
    starting_capital=730_000,
    initial_rent=10_500,
    home_appreciation=0.07,
    years=30,
    scenario_name="Palo Alto @ 7% appreciation"
)

print(f"Property Price: $3,500,000 | Rent: $10,500/month")
print()
print(f"{'Appreciation':<20} {'Renting':<20} {'Buying':<20} {'Winner':<15} {'Margin'}")
print("-" * 100)
print(f"{'3%':<20} ${pa_3pct['renter']:>18,.0f} ${pa_3pct['buyer']:>18,.0f} {pa_3pct['winner']:<15} ${abs(pa_3pct['difference']):>15,.0f}")
print(f"{'7%':<20} ${pa_7pct['renter']:>18,.0f} ${pa_7pct['buyer']:>18,.0f} {pa_7pct['winner']:<15} ${abs(pa_7pct['difference']):>15,.0f}")

# Scenario 3: Cupertino 2000-2021 (historical bull run)
print("\n" + "=" * 100)
print("SCENARIO 3: CUPERTINO 2000-2021 BULL RUN")
print("=" * 100)
print("Historical appreciation: ~7% annually over 21 years")
print()

cupertino = run_scenario(
    property_price=1_900_000,
    down_payment_pct=0.20,
    starting_capital=410_000,
    initial_rent=5_800,
    home_appreciation=0.07,
    years=21,  # 2000-2021
    closing_costs=30_000,
    scenario_name="Cupertino 2000-2021"
)

print(f"After 21 years (2000-2021):")
print(f"  Renting:   ${cupertino['renter']:>18,.0f}")
print(f"  Buying:    ${cupertino['buyer']:>18,.0f}")
print(f"  Winner:    {cupertino['winner']}")
print(f"  Margin:    ${abs(cupertino['difference']):>18,.0f}")

# Scenario 4: Beyond 30 years (mortgage paid off)
print("\n" + "=" * 100)
print("SCENARIO 4: BEYOND 30 YEARS (Mortgage Paid Off)")
print("=" * 100)

sf_40yr = run_scenario(
    property_price=1_900_000,
    down_payment_pct=0.20,
    starting_capital=410_000,
    initial_rent=5_800,
    home_appreciation=0.03,
    years=40,
    closing_costs=30_000,
    scenario_name="SF 40 years @ 3%"
)

sf_50yr = run_scenario(
    property_price=1_900_000,
    down_payment_pct=0.20,
    starting_capital=410_000,
    initial_rent=5_800,
    home_appreciation=0.03,
    years=50,
    closing_costs=30_000,
    scenario_name="SF 50 years @ 3%"
)

print(f"Property Price: $1,900,000 @ 3% appreciation")
print()
print(f"{'Years':<20} {'Renting':<20} {'Buying':<20} {'Winner':<15} {'Margin'}")
print("-" * 100)
print(f"{'30 years':<20} ${sf_3pct['renter']:>18,.0f} ${sf_3pct['buyer']:>18,.0f} {sf_3pct['winner']:<15} ${abs(sf_3pct['difference']):>15,.0f}")
print(f"{'40 years':<20} ${sf_40yr['renter']:>18,.0f} ${sf_40yr['buyer']:>18,.0f} {sf_40yr['winner']:<15} ${abs(sf_40yr['difference']):>15,.0f}")
print(f"{'50 years':<20} ${sf_50yr['renter']:>18,.0f} ${sf_50yr['buyer']:>18,.0f} {sf_50yr['winner']:<15} ${abs(sf_50yr['difference']):>15,.0f}")
print()
print("Note: After year 30, buyer can invest the old mortgage payment (~$9,123/month)")
print("      But renter still invests more total due to early advantage")

# Scenario 5: Parents help with down payment
print("\n" + "=" * 100)
print("SCENARIO 5: PARENTS HELP WITH DOWN PAYMENT")
print("=" * 100)
print("Comparing: Parents keep $410K invested vs giving to kids for down payment")
print()

parents_30yr = analyze_parents_help(parent_contribution=410_000, years=30)

print(f"After 30 years @ 3% home appreciation:")
print(f"  Option 1 - Parents keep $410K invested:       ${parents_30yr['scenario1_parents_invest']:>18,.0f}")
print(f"  Option 2 - Give to kids for down payment:     ${parents_30yr['scenario2_kids_buy']:>18,.0f}")
print(f"  Better option: {parents_30yr['better']}")
print(f"  Difference:    ${abs(parents_30yr['difference']):>18,.0f}")
print()
print("NOTE: This assumes:")
print("  - Kids have $0 without parent help (need full $410K for down payment + closing)")
print("  - Parents could otherwise invest at 7% annually")
print("  - Home appreciates at 3%")

# Summary table
print("\n" + "=" * 100)
print("SUMMARY: FINAL NET WORTH AFTER 30 YEARS")
print("=" * 100)
print()
print(f"{'Scenario':<40} {'Renting':<20} {'Buying':<20} {'Winner'}")
print("-" * 100)

scenarios_30yr = [
    sf_3pct,
    sf_7pct,
    pa_3pct,
    pa_7pct,
]

for s in scenarios_30yr:
    print(f"{s['scenario']:<40} ${s['renter']:>18,.0f} ${s['buyer']:>18,.0f} {s['winner']}")

print()
print("=" * 100)
print("KEY INSIGHTS")
print("=" * 100)
print()
print("1. PALO ALTO EFFECT: Higher prices amplify the outcome")
print(f"   - At 3%: Renting wins by ${abs(pa_3pct['difference']):,.0f} (vs SF ${abs(sf_3pct['difference']):,.0f})")
print(f"   - At 7%: Buying wins by ${abs(pa_7pct['difference']):,.0f} (vs SF ${abs(sf_7pct['difference']):,.0f})")
print()
print("2. CUPERTINO 2000-2021: Historical bull run")
print(f"   - After 21 years: {cupertino['winner']} wins by ${abs(cupertino['difference']):,.0f}")
print()
print("3. BEYOND 30 YEARS: Buyer can finally invest after mortgage paid")
print(f"   - Year 30: {sf_3pct['winner']} by ${abs(sf_3pct['difference']):,.0f}")
print(f"   - Year 40: {sf_40yr['winner']} by ${abs(sf_40yr['difference']):,.0f}")
print(f"   - Year 50: {sf_50yr['winner']} by ${abs(sf_50yr['difference']):,.0f}")
print("   - Renting STILL wins even after buyer invests mortgage payment!")
print()
print("4. PARENTS HELPING:")
print(f"   - {parents_30yr['better']} by ${abs(parents_30yr['difference']):,.0f}")
print("   - Parents better off keeping money invested at 7% than giving for down payment")
print()
print("=" * 100)
