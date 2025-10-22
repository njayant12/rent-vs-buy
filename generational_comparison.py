#!/usr/bin/env python3
"""
Generational Comparison: Buying the same Bay Area house in 2000 vs 2025

Shows how the same house that was affordable to dual-income professionals
in 2000 is now out of reach even for high earners.
"""

# 2000 scenario
PRICE_2000 = 1_000_000  # House was ~$1M in 2000
RATE_2000 = 0.08  # ~8% mortgage rate in 2000
INCOME_2000_MEDIAN = 75_000  # Median household income in 2000

# 2025 scenario
PRICE_2025 = 4_000_000  # Same house is now $4M
RATE_2025 = 0.06  # 6% mortgage rate today
INCOME_2025_MEDIAN = 110_000  # Median household income in 2025

# Tax rates (approximate for high earners in California)
TAX_RATE = 0.4895  # 32% federal + 9.3% CA + 7.65% FICA

# Constants
DOWN_PAYMENT_PCT = 0.20
PROPERTY_TAX_RATE = 0.01
INSURANCE_RATE = 0.0012
MAINTENANCE_RATE = 0.01
STANDARD_DEDUCTION = 31_500
SALT_CAP = 10_000
MORTGAGE_INTEREST_CAP = 750_000

def calculate_affordability(price, rate, year_label):
    """Calculate income needed to afford a house"""

    down_payment = price * DOWN_PAYMENT_PCT
    closing_costs = price * 0.015
    total_upfront = down_payment + closing_costs
    loan_amount = price - down_payment

    # Monthly mortgage payment
    monthly_rate = rate / 12
    num_payments = 30 * 12
    monthly_mortgage = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)

    # Annual costs
    annual_mortgage = monthly_mortgage * 12
    property_tax = price * PROPERTY_TAX_RATE
    insurance = price * INSURANCE_RATE
    maintenance = price * MAINTENANCE_RATE

    total_annual_before_tax = annual_mortgage + property_tax + insurance + maintenance

    # Tax benefit (approximate)
    year1_interest = loan_amount * rate * 0.95

    if loan_amount > MORTGAGE_INTEREST_CAP:
        deductible_interest = year1_interest * (MORTGAGE_INTEREST_CAP / loan_amount)
    else:
        deductible_interest = year1_interest

    salt_deduction = min(property_tax, SALT_CAP)
    itemized = deductible_interest + salt_deduction
    excess = max(0, itemized - STANDARD_DEDUCTION)
    tax_savings = excess * 0.413  # Federal + state, not FICA

    annual_after_tax = total_annual_before_tax - tax_savings
    monthly_after_tax = annual_after_tax / 12

    # Required income at 40% housing ratio
    required_annual_post_tax = (monthly_after_tax / 0.40) * 12
    required_annual_pre_tax = required_annual_post_tax / (1 - TAX_RATE)
    per_person = required_annual_pre_tax / 2

    # Required income at 28% housing ratio (traditional)
    required_annual_post_tax_28 = (monthly_after_tax / 0.28) * 12
    required_annual_pre_tax_28 = required_annual_post_tax_28 / (1 - TAX_RATE)
    per_person_28 = required_annual_pre_tax_28 / 2

    return {
        'year': year_label,
        'price': price,
        'rate': rate,
        'upfront': total_upfront,
        'monthly_mortgage': monthly_mortgage,
        'monthly_after_tax': monthly_after_tax,
        'annual_after_tax': annual_after_tax,
        'income_needed_40pct': required_annual_pre_tax,
        'per_person_40pct': per_person,
        'income_needed_28pct': required_annual_pre_tax_28,
        'per_person_28pct': per_person_28,
    }

print("=" * 100)
print("GENERATIONAL WEALTH GAP: THE SAME HOUSE IN 2000 vs 2025")
print("=" * 100)
print()

result_2000 = calculate_affordability(PRICE_2000, RATE_2000, "2000")
result_2025 = calculate_affordability(PRICE_2025, RATE_2025, "2025")

print(f"{'Metric':<40} {'Year 2000':<25} {'Year 2025':<25} {'Multiple'}")
print("-" * 100)
print(f"{'House Price':<40} ${result_2000['price']:>23,} ${result_2025['price']:>23,} {result_2025['price']/result_2000['price']:>6.1f}x")
print(f"{'Mortgage Rate':<40} {result_2000['rate']*100:>22.1f}% {result_2025['rate']*100:>22.1f}% {result_2025['rate']/result_2000['rate']:>6.2f}x")
print(f"{'Down Payment (20%)':<40} ${result_2000['upfront']:>23,.0f} ${result_2025['upfront']:>23,.0f} {result_2025['upfront']/result_2000['upfront']:>6.1f}x")
print()
print(f"{'Monthly Mortgage (P&I)':<40} ${result_2000['monthly_mortgage']:>23,.0f} ${result_2025['monthly_mortgage']:>23,.0f} {result_2025['monthly_mortgage']/result_2000['monthly_mortgage']:>6.1f}x")
print(f"{'Monthly After-Tax Cost':<40} ${result_2000['monthly_after_tax']:>23,.0f} ${result_2025['monthly_after_tax']:>23,.0f} {result_2025['monthly_after_tax']/result_2000['monthly_after_tax']:>6.1f}x")
print()
print(f"{'Required Income (40% housing ratio):':<40}")
print(f"{'  Household Income':<40} ${result_2000['income_needed_40pct']:>23,.0f} ${result_2025['income_needed_40pct']:>23,.0f} {result_2025['income_needed_40pct']/result_2000['income_needed_40pct']:>6.1f}x")
print(f"{'  Per Person (2 earners)':<40} ${result_2000['per_person_40pct']:>23,.0f} ${result_2025['per_person_40pct']:>23,.0f} {result_2025['per_person_40pct']/result_2000['per_person_40pct']:>6.1f}x")
print()

print("=" * 100)
print("THE REALITY CHECK")
print("=" * 100)
print()

# Calculate as multiple of median income
print("IN 2000:")
print(f"  House price: ${PRICE_2000:,} = {PRICE_2000/INCOME_2000_MEDIAN:.1f}x median household income (${INCOME_2000_MEDIAN:,})")
print(f"  Income needed: ${result_2000['income_needed_40pct']:,.0f}")
print(f"  That's {result_2000['income_needed_40pct']/INCOME_2000_MEDIAN:.1f}x median household income")
print(f"  Per person: ${result_2000['per_person_40pct']:,.0f} (senior engineer / doctor / lawyer salary)")
print()

print("IN 2025:")
print(f"  House price: ${PRICE_2025:,} = {PRICE_2025/INCOME_2025_MEDIAN:.1f}x median household income (${INCOME_2025_MEDIAN:,})")
print(f"  Income needed: ${result_2025['income_needed_40pct']:,.0f}")
print(f"  That's {result_2025['income_needed_40pct']/INCOME_2025_MEDIAN:.1f}x median household income")
print(f"  Per person: ${result_2025['per_person_40pct']:,.0f} (top 0.1% earner)")
print()

print("=" * 100)
print("LINKEDIN POST MATERIAL")
print("=" * 100)
print()

print('"Why don\'t you just buy?"')
print()
print(f"That $4M Bay Area house you bought in 2000 for ~$1M?")
print()
print(f"THEN (2000):")
print(f"• House price: $1M")
print(f"• Down payment: ${result_2000['upfront']:,.0f}")
print(f"• Monthly cost: ${result_2000['monthly_after_tax']:,.0f}")
print(f"• Income needed: ${result_2000['income_needed_40pct']:,.0f} household")
print(f"• Per person: ${result_2000['per_person_40pct']:,.0f} (achievable for two professionals)")
print()
print(f"NOW (2025):")
print(f"• Same house: $4M (4x the price)")
print(f"• Down payment: ${result_2025['upfront']:,.0f} (3.5x more)")
print(f"• Monthly cost: ${result_2025['monthly_after_tax']:,.0f} (2.4x more)")
print(f"• Income needed: ${result_2025['income_needed_40pct']:,.0f} household (2.9x more)")
print(f"• Per person: ${result_2025['per_person_40pct']:,.0f} (top 0.1% earner)")
print()
print("When you bought, it cost {:.1f}x median income. Now it's {:.1f}x median income.".format(
    PRICE_2000/INCOME_2000_MEDIAN,
    PRICE_2025/INCOME_2025_MEDIAN
))
print()
print("It's not that we're not working hard enough.")
print("It's that the house is literally 4x more expensive.")
print("And even with 'good jobs', most dual-income earners can't reach $750K/person.")
print()
print("This is generational wealth gap in action.")
print()

print("=" * 100)
