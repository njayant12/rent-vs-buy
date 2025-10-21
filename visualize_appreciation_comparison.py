#!/usr/bin/env python3
"""
30-Year Rent vs Buy - Multiple Appreciation Scenarios
Compare 3%, 5%, and 7% home appreciation rates
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

def run_scenario(home_appreciation_rate):
    """Run 30-year analysis for a given home appreciation rate"""
    # Initialize
    down_3pct = PROPERTY_PRICE * 0.03
    loan_3pct = PROPERTY_PRICE - down_3pct
    monthly_payment_3pct = calculate_monthly_mortgage_payment(loan_3pct, MORTGAGE_RATE)
    monthly_pmi_3pct = (PROPERTY_PRICE * PMI_RATE) / 12
    monthly_tax_ins = (PROPERTY_PRICE * PROPERTY_TAX_RATE + HOME_INSURANCE_ANNUAL) / 12
    baseline_monthly = monthly_payment_3pct + monthly_pmi_3pct + monthly_tax_ins

    down_20pct = PROPERTY_PRICE * 0.20
    loan_20pct = PROPERTY_PRICE - down_20pct
    monthly_payment_20pct = calculate_monthly_mortgage_payment(loan_20pct, MORTGAGE_RATE)
    monthly_savings_20pct = baseline_monthly - (monthly_payment_20pct + monthly_tax_ins)

    investment_3pct = STARTING_CAPITAL - down_3pct - CLOSING_COSTS
    mortgage_balance_3pct = loan_3pct

    investment_20pct = 0
    mortgage_balance_20pct = loan_20pct

    monthly_savings_rent = baseline_monthly - MONTHLY_RENT
    investment_rent = STARTING_CAPITAL

    property_value = PROPERTY_PRICE
    property_tax = PROPERTY_PRICE * PROPERTY_TAX_RATE
    home_insurance = HOME_INSURANCE_ANNUAL

    years = []
    net_worth_rent_data = []
    net_worth_3_data = []
    net_worth_20_data = []

    for year in range(1, 31):
        property_value = property_value * (1 + home_appreciation_rate)
        property_tax = property_tax * 1.02
        home_insurance = home_insurance * 1.03

        # 3% DOWN
        interest_3, principal_3, mortgage_balance_3pct = calculate_year_mortgage_breakdown(
            mortgage_balance_3pct, monthly_payment_3pct)
        equity_pct_3 = (property_value - mortgage_balance_3pct) / PROPERTY_PRICE
        pmi_3 = 0 if equity_pct_3 >= 0.20 else PROPERTY_PRICE * PMI_RATE

        investment_3pct = calculate_investment_growth_with_contributions(investment_3pct, 0, 12)
        home_equity_3 = property_value - mortgage_balance_3pct
        net_worth_3 = investment_3pct + home_equity_3

        # 20% DOWN
        interest_20, principal_20, mortgage_balance_20pct = calculate_year_mortgage_breakdown(
            mortgage_balance_20pct, monthly_payment_20pct)

        investment_20pct = calculate_investment_growth_with_contributions(
            investment_20pct, monthly_savings_20pct, 12)
        home_equity_20 = property_value - mortgage_balance_20pct
        net_worth_20 = investment_20pct + home_equity_20

        # RENTING
        investment_rent = calculate_investment_growth_with_contributions(
            investment_rent, monthly_savings_rent, 12)
        net_worth_rent = investment_rent

        years.append(year)
        net_worth_rent_data.append(net_worth_rent)
        net_worth_3_data.append(net_worth_3)
        net_worth_20_data.append(net_worth_20)

    return years, net_worth_rent_data, net_worth_3_data, net_worth_20_data

# Run all three scenarios
print("Running scenarios...")
years_3, rent_3, down3_3, down20_3 = run_scenario(0.03)
years_5, rent_5, down3_5, down20_5 = run_scenario(0.05)
years_7, rent_7, down3_7, down20_7 = run_scenario(0.07)

# Create subplot with 3 graphs
fig, axes = plt.subplots(1, 3, figsize=(20, 6))

# 3% Appreciation
ax1 = axes[0]
ax1.plot(years_3, rent_3, linewidth=2.5, label='Renting', color='#10b981')
ax1.plot(years_3, down20_3, linewidth=2.5, label='20% Down', color='#3b82f6')
ax1.plot(years_3, down3_3, linewidth=2.5, label='3% Down', color='#f59e0b')
ax1.set_title('3% Home Appreciation', fontsize=14, fontweight='bold')
ax1.set_xlabel('Year', fontsize=11)
ax1.set_ylabel('Net Worth ($)', fontsize=11)
ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax1.grid(True, alpha=0.3, linestyle='--')
ax1.legend(fontsize=10)
ax1.annotate(f'Rent: ${rent_3[-1]/1e6:.1f}M', xy=(30, rent_3[-1]),
             xytext=(-80, 10), textcoords='offset points', fontsize=9, color='#10b981')
ax1.annotate(f'20%: ${down20_3[-1]/1e6:.1f}M', xy=(30, down20_3[-1]),
             xytext=(-80, -15), textcoords='offset points', fontsize=9, color='#3b82f6')

# 5% Appreciation
ax2 = axes[1]
ax2.plot(years_5, rent_5, linewidth=2.5, label='Renting', color='#10b981')
ax2.plot(years_5, down20_5, linewidth=2.5, label='20% Down', color='#3b82f6')
ax2.plot(years_5, down3_5, linewidth=2.5, label='3% Down', color='#f59e0b')
ax2.set_title('5% Home Appreciation', fontsize=14, fontweight='bold')
ax2.set_xlabel('Year', fontsize=11)
ax2.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax2.grid(True, alpha=0.3, linestyle='--')
ax2.legend(fontsize=10)
ax2.annotate(f'Rent: ${rent_5[-1]/1e6:.1f}M', xy=(30, rent_5[-1]),
             xytext=(-80, 10), textcoords='offset points', fontsize=9, color='#10b981')
ax2.annotate(f'20%: ${down20_5[-1]/1e6:.1f}M', xy=(30, down20_5[-1]),
             xytext=(-80, -15), textcoords='offset points', fontsize=9, color='#3b82f6')

# 7% Appreciation
ax3 = axes[2]
ax3.plot(years_7, rent_7, linewidth=2.5, label='Renting', color='#10b981')
ax3.plot(years_7, down20_7, linewidth=2.5, label='20% Down', color='#3b82f6')
ax3.plot(years_7, down3_7, linewidth=2.5, label='3% Down', color='#f59e0b')
ax3.set_title('7% Home Appreciation', fontsize=14, fontweight='bold')
ax3.set_xlabel('Year', fontsize=11)
ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M'))
ax3.grid(True, alpha=0.3, linestyle='--')
ax3.legend(fontsize=10)
ax3.annotate(f'20%: ${down20_7[-1]/1e6:.1f}M', xy=(30, down20_7[-1]),
             xytext=(-80, 10), textcoords='offset points', fontsize=9, color='#3b82f6')
ax3.annotate(f'Rent: ${rent_7[-1]/1e6:.1f}M', xy=(30, rent_7[-1]),
             xytext=(-80, -15), textcoords='offset points', fontsize=9, color='#10b981')

fig.suptitle('30-Year Net Worth: Impact of Home Appreciation Rate\n$1.9M SF Property | 7% Investment Return',
             fontsize=16, fontweight='bold', y=1.02)

plt.tight_layout()
plt.savefig('appreciation_comparison.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'appreciation_comparison.png'")

print(f"\n{'='*80}")
print("FINAL NET WORTH COMPARISON (30 YEARS)")
print(f"{'='*80}")
print(f"\n3% Home Appreciation:")
print(f"  Renting:   ${rent_3[-1]:>14,.0f}")
print(f"  20% Down:  ${down20_3[-1]:>14,.0f}")
print(f"  3% Down:   ${down3_3[-1]:>14,.0f}")
print(f"  Winner: {'Renting' if rent_3[-1] > down20_3[-1] else '20% Down'} (by ${abs(rent_3[-1] - down20_3[-1]):,.0f})")

print(f"\n5% Home Appreciation:")
print(f"  Renting:   ${rent_5[-1]:>14,.0f}")
print(f"  20% Down:  ${down20_5[-1]:>14,.0f}")
print(f"  3% Down:   ${down3_5[-1]:>14,.0f}")
print(f"  Winner: {'Renting' if rent_5[-1] > down20_5[-1] else '20% Down'} (by ${abs(rent_5[-1] - down20_5[-1]):,.0f})")

print(f"\n7% Home Appreciation:")
print(f"  Renting:   ${rent_7[-1]:>14,.0f}")
print(f"  20% Down:  ${down20_7[-1]:>14,.0f}")
print(f"  3% Down:   ${down3_7[-1]:>14,.0f}")
print(f"  Winner: {'Renting' if rent_7[-1] > down20_7[-1] else '20% Down'} (by ${abs(rent_7[-1] - down20_7[-1]):,.0f})")
print(f"{'='*80}")
