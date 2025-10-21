#!/usr/bin/env python3
"""
30-Year Rent vs Buy Visualization
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# Constants
PROPERTY_PRICE = 1_900_000
MONTHLY_RENT = 5_800
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

    total_contributions = monthly_contribution * months
    total_returns = balance - starting_balance - total_contributions

    return balance, total_contributions, total_returns

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

# Initialize scenarios
down_3pct = PROPERTY_PRICE * 0.03
loan_3pct = PROPERTY_PRICE - down_3pct
monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)
monthly_pmi_3pct = (PROPERTY_PRICE * PMI_RATE) / 12
monthly_tax_ins = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12
baseline_monthly = monthly_payment_3pct + monthly_pmi_3pct + monthly_tax_ins

upfront_3pct = down_3pct + CLOSING_COSTS
investment_3pct = STARTING_CAPITAL - upfront_3pct
mortgage_balance_3pct = loan_3pct

down_20pct = PROPERTY_PRICE * 0.20
loan_20pct = PROPERTY_PRICE - down_20pct
monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)
monthly_savings_20pct = baseline_monthly - (monthly_payment_20pct + monthly_tax_ins)

upfront_20pct = down_20pct + CLOSING_COSTS
investment_20pct = 0
mortgage_balance_20pct = loan_20pct

monthly_savings_rent = baseline_monthly - MONTHLY_RENT
investment_rent = STARTING_CAPITAL

property_value = PROPERTY_PRICE
property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE
home_insurance = HOME_INSURANCE_ANNUAL
annual_rent = MONTHLY_RENT * 12

# Track data
years = []
net_worth_rent_data = []
net_worth_3_data = []
net_worth_20_data = []

for year in range(1, 31):
    property_value = property_value * (1 + HOME_APPRECIATION)
    property_tax = property_tax * 1.02
    home_insurance = home_insurance * 1.03
    annual_rent = annual_rent * (1 + RENT_GROWTH)

    # 3% DOWN
    interest_3, principal_3, mortgage_balance_3pct = calculate_year_mortgage_breakdown(
        mortgage_balance_3pct, monthly_payment_3pct)
    equity_pct_3 = (property_value - mortgage_balance_3pct) / PROPERTY_PRICE
    pmi_3 = 0 if equity_pct_3 >= 0.20 else PROPERTY_PRICE * PMI_RATE
    total_costs_3 = (monthly_payment_3pct * 12) + property_tax + home_insurance + pmi_3
    tax_savings_3 = calculate_tax_benefit(interest_3, property_tax,
                                          loan_3pct if year == 1 else mortgage_balance_3pct)
    investment_3pct, _, _ = calculate_investment_growth_with_contributions(investment_3pct, 0, 12)
    home_equity_3 = property_value - mortgage_balance_3pct
    net_worth_3 = investment_3pct + home_equity_3

    # 20% DOWN
    interest_20, principal_20, mortgage_balance_20pct = calculate_year_mortgage_breakdown(
        mortgage_balance_20pct, monthly_payment_20pct)
    total_costs_20 = (monthly_payment_20pct * 12) + property_tax + home_insurance
    tax_savings_20 = calculate_tax_benefit(interest_20, property_tax,
                                           loan_20pct if year == 1 else mortgage_balance_20pct)
    investment_20pct, _, _ = calculate_investment_growth_with_contributions(
        investment_20pct, monthly_savings_20pct, 12)
    home_equity_20 = property_value - mortgage_balance_20pct
    net_worth_20 = investment_20pct + home_equity_20

    # RENTING
    investment_rent, _, _ = calculate_investment_growth_with_contributions(
        investment_rent, monthly_savings_rent, 12)
    net_worth_rent = investment_rent

    years.append(year)
    net_worth_rent_data.append(net_worth_rent)
    net_worth_3_data.append(net_worth_3)
    net_worth_20_data.append(net_worth_20)

# Create the plot
plt.figure(figsize=(14, 8))
plt.plot(years, net_worth_rent_data, linewidth=2.5, label='Renting', color='#10b981', marker='o', markersize=4)
plt.plot(years, net_worth_20_data, linewidth=2.5, label='20% Down', color='#3b82f6', marker='s', markersize=4)
plt.plot(years, net_worth_3_data, linewidth=2.5, label='3% Down + PMI', color='#f59e0b', marker='^', markersize=4)

plt.title('30-Year Net Worth: Rent vs Buy\n$1.9M SF Property | 3% Home Appreciation | 7% Investment Return',
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
plt.annotate(f'${net_worth_rent_data[-1]/1e6:.1f}M',
             xy=(final_year, net_worth_rent_data[-1]),
             xytext=(10, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#10b981')
plt.annotate(f'${net_worth_20_data[-1]/1e6:.1f}M',
             xy=(final_year, net_worth_20_data[-1]),
             xytext=(10, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#3b82f6')
plt.annotate(f'${net_worth_3_data[-1]/1e6:.1f}M',
             xy=(final_year, net_worth_3_data[-1]),
             xytext=(10, 0), textcoords='offset points',
             fontsize=11, fontweight='bold', color='#f59e0b')

plt.tight_layout()
plt.savefig('rent_vs_buy_30year.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'rent_vs_buy_30year.png'")
print(f"\nFinal Net Worth After 30 Years:")
print(f"  Renting:   ${net_worth_rent_data[-1]:,.0f}")
print(f"  20% Down:  ${net_worth_20_data[-1]:,.0f}")
print(f"  3% Down:   ${net_worth_3_data[-1]:,.0f}")
