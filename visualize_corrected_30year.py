#!/usr/bin/env python3
"""
30-Year Visualization - CORRECTED BASELINE
Shows net worth trajectories with correct baseline income methodology
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Constants
PROPERTY_PRICE = 1_900_000
MONTHLY_RENT_INITIAL = 5_800
STARTING_CAPITAL = 410_000
MORTGAGE_RATE = 0.06
PROPERTY_TAX_RATE = 0.012
HOME_INSURANCE_ANNUAL = 3_000
CLOSING_COSTS = 30_000
RENT_GROWTH = 0.03
HOME_APPRECIATION = 0.03
INVESTMENT_RETURN = 0.07
TAX_RATE = 0.413
STANDARD_DEDUCTION = 31_500
MORTGAGE_INTEREST_CAP = 750_000
SALT_CAP = 10_000
PMI_RATE = 0.01

def calculate_monthly_mortgage_payment(principal, annual_rate, years=30):
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / \
              ((1 + monthly_rate)**num_payments - 1)
    return payment

def calculate_year_mortgage_breakdown(principal_remaining, monthly_payment):
    monthly_rate = MORTGAGE_RATE / 12
    interest_paid = 0
    principal_paid = 0
    balance = principal_remaining

    for month in range(12):
        interest_this_month = balance * monthly_rate
        principal_this_month = monthly_payment - interest_this_month
        interest_paid += interest_this_month
        principal_paid += principal_this_month
        balance -= principal_this_month

    return interest_paid, principal_paid, balance

def calculate_investment_growth_with_contributions(starting_balance, monthly_contribution, months=12):
    monthly_rate = INVESTMENT_RETURN / 12
    balance = starting_balance

    for month in range(months):
        balance = balance * (1 + monthly_rate)
        balance += monthly_contribution

    return balance

def calculate_tax_benefit(mortgage_interest, property_tax, loan_amount):
    if loan_amount > MORTGAGE_INTEREST_CAP:
        deductible_interest = mortgage_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
    else:
        deductible_interest = mortgage_interest

    salt_deduction = min(property_tax, SALT_CAP)
    itemized = deductible_interest + salt_deduction
    excess = max(0, itemized - STANDARD_DEDUCTION)
    tax_savings = excess * TAX_RATE

    return tax_savings

def run_scenario():
    """Run 30-year analysis with correct baseline"""
    # Initialize
    down_3pct = PROPERTY_PRICE * 0.03
    loan_3pct = PROPERTY_PRICE - down_3pct
    monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)

    investment_3pct = STARTING_CAPITAL - down_3pct - CLOSING_COSTS
    mortgage_balance_3pct = loan_3pct

    down_20pct = PROPERTY_PRICE * 0.20
    loan_20pct = PROPERTY_PRICE - down_20pct
    monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)

    investment_20pct = STARTING_CAPITAL - down_20pct - CLOSING_COSTS
    mortgage_balance_20pct = loan_20pct

    investment_rent = STARTING_CAPITAL

    property_value = PROPERTY_PRICE
    property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE
    home_insurance = HOME_INSURANCE_ANNUAL
    annual_rent = MONTHLY_RENT_INITIAL * 12

    years = []
    net_worth_rent_data = []
    net_worth_3_data = []
    net_worth_20_data = []

    for year in range(1, 31):
        property_value = property_value * (1 + HOME_APPRECIATION)
        property_tax = property_tax * 1.02
        home_insurance = home_insurance * 1.03
        annual_rent = annual_rent * (1 + RENT_GROWTH)

        # 3% DOWN - Calculate baseline
        interest_3, principal_3, mortgage_balance_3pct = calculate_year_mortgage_breakdown(
            mortgage_balance_3pct, monthly_payment_3pct)

        equity_pct_3 = (property_value - mortgage_balance_3pct) / PROPERTY_PRICE
        pmi_3_annual = 0 if equity_pct_3 >= 0.20 else PROPERTY_PRICE * PMI_RATE

        costs_3_before_tax = (monthly_payment_3pct * 12) + property_tax + home_insurance + pmi_3_annual
        tax_savings_3 = calculate_tax_benefit(interest_3, property_tax,
                                              loan_3pct if year == 1 else mortgage_balance_3pct)
        costs_3_after_tax = costs_3_before_tax - tax_savings_3
        baseline_monthly_income = costs_3_after_tax / 12

        # 20% DOWN
        interest_20, principal_20, mortgage_balance_20pct = calculate_year_mortgage_breakdown(
            mortgage_balance_20pct, monthly_payment_20pct)

        costs_20_before_tax = (monthly_payment_20pct * 12) + property_tax + home_insurance
        tax_savings_20 = calculate_tax_benefit(interest_20, property_tax,
                                               loan_20pct if year == 1 else mortgage_balance_20pct)
        costs_20_after_tax = costs_20_before_tax - tax_savings_20
        monthly_20_spending = costs_20_after_tax / 12
        monthly_savings_20 = baseline_monthly_income - monthly_20_spending

        # RENTING
        monthly_rent = annual_rent / 12
        monthly_savings_rent = baseline_monthly_income - monthly_rent

        # INVESTMENT GROWTH
        investment_3pct = calculate_investment_growth_with_contributions(investment_3pct, 0, 12)
        investment_20pct = calculate_investment_growth_with_contributions(
            investment_20pct, monthly_savings_20, 12)
        investment_rent = calculate_investment_growth_with_contributions(
            investment_rent, monthly_savings_rent, 12)

        # NET WORTH
        home_equity_3 = property_value - mortgage_balance_3pct
        net_worth_3 = investment_3pct + home_equity_3

        home_equity_20 = property_value - mortgage_balance_20pct
        net_worth_20 = investment_20pct + home_equity_20

        net_worth_rent = investment_rent

        years.append(year)
        net_worth_rent_data.append(net_worth_rent)
        net_worth_3_data.append(net_worth_3)
        net_worth_20_data.append(net_worth_20)

    return years, net_worth_rent_data, net_worth_3_data, net_worth_20_data

# Run the analysis
print("Generating corrected 30-year visualization...")
years, rent_data, down3_data, down20_data = run_scenario()

# Create the plot
plt.figure(figsize=(14, 8))
plt.plot(years, rent_data, linewidth=3, label='Renting', color='#10b981', marker='o', markersize=3)
plt.plot(years, down20_data, linewidth=3, label='20% Down', color='#3b82f6', marker='s', markersize=3)
plt.plot(years, down3_data, linewidth=3, label='3% Down + PMI', color='#f59e0b', marker='^', markersize=3)

plt.title('30-Year Net Worth: Rent vs Buy (CORRECTED)\n$1.9M SF Property | 3% Home Appreciation | 7% Investment Return',
          fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Year', fontsize=13, fontweight='bold')
plt.ylabel('Net Worth ($)', fontsize=13, fontweight='bold')

# Format y-axis as millions
ax = plt.gca()
ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))

plt.grid(True, alpha=0.3, linestyle='--')
plt.legend(fontsize=12, loc='upper left', framealpha=0.9)

# Add final values as annotations
final_year = 30
plt.annotate(f'${rent_data[-1]/1e6:.1f}M',
             xy=(final_year, rent_data[-1]),
             xytext=(10, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#10b981')
plt.annotate(f'${down20_data[-1]/1e6:.1f}M',
             xy=(final_year, down20_data[-1]),
             xytext=(10, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#3b82f6')
plt.annotate(f'${down3_data[-1]/1e6:.1f}M',
             xy=(final_year, down3_data[-1]),
             xytext=(10, -15), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#f59e0b')

# Add note about correction
plt.text(0.5, 0.02, 'Note: Uses correct baseline (income = 3% down spending)',
         ha='center', va='bottom', transform=plt.gcf().transFigure,
         fontsize=10, style='italic', color='#666')

plt.tight_layout()
plt.savefig('rent_vs_buy_30year_CORRECTED.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'rent_vs_buy_30year_CORRECTED.png'")
print(f"\nFinal Net Worth After 30 Years:")
print(f"  Renting:   ${rent_data[-1]:,.0f}")
print(f"  20% Down:  ${down20_data[-1]:,.0f}")
print(f"  3% Down:   ${down3_data[-1]:,.0f}")
print(f"\nRenting wins by ${rent_data[-1] - max(down20_data[-1], down3_data[-1]):,.0f}")
