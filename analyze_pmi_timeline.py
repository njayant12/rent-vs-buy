#!/usr/bin/env python3
"""
Track PMI over time for 3% down scenario
Show when it's removed and the impact
"""

PROPERTY_PRICE = 1_900_000
MORTGAGE_RATE = 0.06
PMI_RATE = 0.01
HOME_APPRECIATION = 0.03

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

print("="*90)
print("PMI TIMELINE FOR 3% DOWN SCENARIO")
print("="*90)

# 3% down setup
down_payment = PROPERTY_PRICE * 0.03
loan_amount = PROPERTY_PRICE - down_payment
monthly_payment = calculate_monthly_mortgage_payment(loan_amount, MORTGAGE_RATE)

print(f"\nINITIAL SETUP:")
print(f"  Purchase Price: ${PROPERTY_PRICE:,}")
print(f"  Down Payment (3%): ${down_payment:,}")
print(f"  Loan Amount: ${loan_amount:,}")
print(f"  Monthly P&I: ${monthly_payment:,.2f}")
print(f"  Annual PMI (1% of purchase): ${PROPERTY_PRICE * PMI_RATE:,}")
print(f"  Monthly PMI: ${(PROPERTY_PRICE * PMI_RATE)/12:,.2f}")

print(f"\n{'='*90}")
print(f"YEAR-BY-YEAR PMI TRACKING")
print(f"{'='*90}")
print(f"\n{'Year':<6} {'Property Value':<16} {'Loan Balance':<16} {'Total Equity':<16} " +
      f"{'Equity %':<12} {'PMI Status':<20} {'Annual PMI':<12}")
print("-" * 90)

property_value = PROPERTY_PRICE
mortgage_balance = loan_amount
cumulative_pmi = 0

for year in range(1, 11):
    # Calculate this year's mortgage payments
    interest, principal, mortgage_balance = calculate_year_mortgage_breakdown(
        mortgage_balance, monthly_payment)

    # Update property value with appreciation
    property_value = property_value * (1 + HOME_APPRECIATION)

    # Calculate equity
    total_equity = property_value - mortgage_balance

    # Calculate equity percentage (based on ORIGINAL purchase price)
    equity_pct = total_equity / PROPERTY_PRICE

    # Determine if PMI applies (need 20% equity based on original price)
    if equity_pct >= 0.20:
        pmi_status = "✓ REMOVED"
        annual_pmi = 0
    else:
        pmi_status = "Paying PMI"
        annual_pmi = PROPERTY_PRICE * PMI_RATE
        cumulative_pmi += annual_pmi

    print(f"{year:<6} ${property_value:>14,.0f} ${mortgage_balance:>14,.0f} ${total_equity:>14,.0f} " +
          f"{equity_pct*100:>10.1f}% {pmi_status:<20} ${annual_pmi:>10,}")

print("-" * 90)
print(f"\nTOTAL PMI PAID: ${cumulative_pmi:,.0f}")

print(f"\n{'='*90}")
print("DETAILED BREAKDOWN OF PMI REMOVAL")
print(f"{'='*90}")

# Re-run to show the critical years
property_value = PROPERTY_PRICE
mortgage_balance = loan_amount

print("\nYEAR 3 (Last year with PMI):")
for year in range(1, 4):
    interest, principal, mortgage_balance = calculate_year_mortgage_breakdown(
        mortgage_balance, monthly_payment)
    property_value = property_value * (1 + HOME_APPRECIATION)

total_equity_y3 = property_value - mortgage_balance
equity_pct_y3 = total_equity_y3 / PROPERTY_PRICE

print(f"  Property Value: ${property_value:,.0f}")
print(f"  Loan Balance: ${mortgage_balance:,.0f}")
print(f"  Total Equity: ${total_equity_y3:,.0f}")
print(f"  Equity %: {equity_pct_y3*100:.2f}% of original purchase price")
print(f"  Status: {equity_pct_y3*100:.2f}% < 20% → Still paying PMI")

# Year 4
interest, principal, mortgage_balance = calculate_year_mortgage_breakdown(
    mortgage_balance, monthly_payment)
property_value = property_value * (1 + HOME_APPRECIATION)
total_equity_y4 = property_value - mortgage_balance
equity_pct_y4 = total_equity_y4 / PROPERTY_PRICE

print("\nYEAR 4 (PMI removed):")
print(f"  Property Value: ${property_value:,.0f}")
print(f"  Loan Balance: ${mortgage_balance:,.0f}")
print(f"  Total Equity: ${total_equity_y4:,.0f}")
print(f"  Equity %: {equity_pct_y4*100:.2f}% of original purchase price")
print(f"  Status: {equity_pct_y4*100:.2f}% >= 20% → ✓ PMI REMOVED!")

print(f"\n{'='*90}")
print("IMPACT ON BASELINE INCOME")
print(f"{'='*90}")

# This affects the baseline income for ALL scenarios
print("\nYEAR 3 BASELINE (with PMI):")
print(f"  3% down annual costs (before tax): ~$177,400")
print(f"    Mortgage P&I: $132,600")
print(f"    Property Tax: $23,700")
print(f"    Insurance: $3,100")
print(f"    PMI: $19,000 ← INCLUDED")
print(f"  After tax (~$15K benefit): ~$162,400")
print(f"  Monthly baseline income: ~$13,533")

print("\nYEAR 4 BASELINE (no PMI):")
print(f"  3% down annual costs (before tax): ~$158,700")
print(f"    Mortgage P&I: $132,600")
print(f"    Property Tax: $24,200")
print(f"    Insurance: $3,200")
print(f"    PMI: $0 ← REMOVED!")
print(f"  After tax (~$15K benefit): ~$143,700")
print(f"  Monthly baseline income: ~$11,975")
print(f"\n  BASELINE DROP: ~$1,558/month when PMI removed!")

print(f"\n{'='*90}")
print("IMPACT ON ALL THREE SCENARIOS")
print(f"{'='*90}")

print("\nWhen PMI is removed in Year 4, baseline income drops ~$1,558/month")
print("\nThis affects everyone:")
print("  3% down: Income drops, still invests $0")
print("  20% down: Income drops → can invest less")
print("  Renter: Income drops → can invest less")
print("\nBut the impact varies:")
print("  20% down: $3,520 → $1,937 (drops $1,583)")
print("  Renter: $8,054 → $6,038 (drops $2,016)")

print(f"\n{'='*90}")
print("KEY INSIGHTS")
print(f"{'='*90}")

print(f"\n1. PMI is paid for ONLY 3 YEARS (years 1-3)")
print(f"   Total cost: ${cumulative_pmi:,.0f}")

print(f"\n2. PMI removal threshold: 20% equity in home")
print(f"   Calculated based on ORIGINAL purchase price")
print(f"   Not based on current market value")

print(f"\n3. Year 4 is the inflection point:")
print(f"   - PMI drops from $19,000/year to $0")
print(f"   - Baseline income drops ~$1,558/month")
print(f"   - All scenarios see reduced investment capacity")

print(f"\n4. The early PMI years (1-3) actually HELP the renter!")
print(f"   - PMI inflates baseline income to ~$14,028/month")
print(f"   - This lets renter invest $8,054/month")
print(f"   - Without PMI, renter would only invest ~$6,500/month")
print(f"   - So 3% down paying PMI actually subsidizes the renter's gains!")

print("="*90)
