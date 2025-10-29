#!/usr/bin/env python3
"""
Monthly Cost Analysis WITH Tax Benefits: Jubilee vs 20% Down vs Renting
Includes federal and California state tax deductions

NEW: Adds mortgage interest deduction and SALT deduction benefits
"""

import math

# ============================================================================
# ASSUMPTIONS
# ============================================================================

HOME_PRICE = 1_900_000

# Interest rates
FHA_RATE = 0.0625
CONVENTIONAL_RATE = 0.0615

# Property tax
PROPERTY_TAX_RATE = 0.0118
ANNUAL_INSURANCE = 1_500
MAINTENANCE_RATE = 0.01

# Jubilee model
LAND_SHARE = 0.60
HOUSE_SHARE = 0.40
LAND_VALUE = HOME_PRICE * LAND_SHARE
HOUSE_VALUE = HOME_PRICE * HOUSE_SHARE

# Land lease - verified 7% based on ~$3,500/mo for $1M
LAND_LEASE_RATE = 0.07
ANNUAL_LAND_LEASE = LAND_VALUE * LAND_LEASE_RATE

# FHA loan details
FHA_DOWN_PCT = 0.035
FHA_UPFRONT_PMI = 0.0175
FHA_ANNUAL_PMI_RATE = 0.0055

# Traditional loan
TRADITIONAL_DOWN_PCT = 0.20

# Renting
MONTHLY_RENT = 5_800
RENTERS_INSURANCE_ANNUAL = 200

# ============================================================================
# TAX ASSUMPTIONS (NEW)
# ============================================================================

# Married Filing Jointly
FEDERAL_TAX_RATE = 0.24  # 24% bracket (reasonable for $1.9M home buyer)
CA_TAX_RATE = 0.093  # 9.3% bracket

# Standard deductions (2025 estimates)
FEDERAL_STANDARD_DEDUCTION = 29_200
CA_STANDARD_DEDUCTION = 10_726

# SALT assumptions
TOTAL_SALT = 40_000  # Total state/local taxes (state income tax + property tax)
FEDERAL_SALT_CAP = 10_000  # Federal cap

# Mortgage interest deduction limit (federal)
MORTGAGE_DEBT_LIMIT = 750_000  # Can only deduct interest on first $750k

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def calculate_mortgage_payment(principal, annual_rate, years=30):
    """Calculate monthly mortgage payment (P&I)"""
    monthly_rate = annual_rate / 12
    n_payments = years * 12
    if monthly_rate == 0:
        return principal / n_payments
    payment = principal * (monthly_rate * (1 + monthly_rate)**n_payments) / \
              ((1 + monthly_rate)**n_payments - 1)
    return payment

def calculate_first_year_interest(principal, annual_rate):
    """Calculate first year mortgage interest (simple: principal × rate)

    This is accurate for year 1 since principal barely decreases"""
    return principal * annual_rate

print("=" * 95)
print("MONTHLY COST ANALYSIS WITH TAX BENEFITS")
print("$1.9M San Francisco Home - Married Filing Jointly")
print("=" * 95)
print()

# ============================================================================
# SCENARIO 1: JUBILEE
# ============================================================================

print("=" * 95)
print("SCENARIO 1: JUBILEE")
print("=" * 95)
print()

# Loan details
jubilee_down_payment = HOUSE_VALUE * FHA_DOWN_PCT
jubilee_loan_before_pmi = HOUSE_VALUE - jubilee_down_payment
jubilee_upfront_pmi = jubilee_loan_before_pmi * FHA_UPFRONT_PMI
jubilee_total_loan = jubilee_loan_before_pmi + jubilee_upfront_pmi

# Monthly costs
jubilee_mortgage = calculate_mortgage_payment(jubilee_total_loan, FHA_RATE)
jubilee_annual_pmi = jubilee_loan_before_pmi * FHA_ANNUAL_PMI_RATE
jubilee_monthly_pmi = jubilee_annual_pmi / 12
jubilee_monthly_land_lease = ANNUAL_LAND_LEASE / 12
jubilee_annual_property_tax = HOME_PRICE * PROPERTY_TAX_RATE
jubilee_monthly_property_tax = jubilee_annual_property_tax / 12
jubilee_monthly_insurance = ANNUAL_INSURANCE / 12
jubilee_annual_maintenance = HOME_PRICE * MAINTENANCE_RATE
jubilee_monthly_maintenance = jubilee_annual_maintenance / 12

jubilee_pretax_monthly = (jubilee_mortgage + jubilee_monthly_pmi +
                          jubilee_monthly_land_lease + jubilee_monthly_property_tax +
                          jubilee_monthly_insurance + jubilee_monthly_maintenance)

# TAX BENEFITS
print("TAX DEDUCTION CALCULATION:")
print()

# Calculate first year mortgage interest
jubilee_annual_interest = calculate_first_year_interest(jubilee_total_loan, FHA_RATE)
print(f"  First year mortgage interest: ${jubilee_annual_interest:,.0f}")

# Federal deductions
jubilee_federal_mortgage_interest = min(jubilee_annual_interest,
                                       calculate_first_year_interest(MORTGAGE_DEBT_LIMIT, FHA_RATE))
jubilee_federal_itemized = jubilee_federal_mortgage_interest + FEDERAL_SALT_CAP
jubilee_federal_extra_deduction = max(0, jubilee_federal_itemized - FEDERAL_STANDARD_DEDUCTION)
jubilee_federal_tax_savings_annual = jubilee_federal_extra_deduction * FEDERAL_TAX_RATE
jubilee_federal_tax_savings_monthly = jubilee_federal_tax_savings_annual / 12

print()
print(f"Federal Tax Benefit:")
print(f"  Mortgage interest (deductible): ${jubilee_federal_mortgage_interest:,.0f}")
print(f"  SALT deduction (capped):        ${FEDERAL_SALT_CAP:,.0f}")
print(f"  Total itemized:                 ${jubilee_federal_itemized:,.0f}")
print(f"  vs Standard deduction:          ${FEDERAL_STANDARD_DEDUCTION:,.0f}")
print(f"  Extra deduction:                ${jubilee_federal_extra_deduction:,.0f}")
print(f"  Tax savings @ {FEDERAL_TAX_RATE*100:.0f}%:         ${jubilee_federal_tax_savings_annual:,.0f}/year")
print(f"  Monthly benefit:                ${jubilee_federal_tax_savings_monthly:,.0f}/month")

# California deductions (no mortgage debt limit, full SALT deduction)
jubilee_state_income_tax = TOTAL_SALT - jubilee_annual_property_tax
jubilee_ca_itemized = jubilee_annual_interest + jubilee_annual_property_tax + jubilee_state_income_tax
jubilee_ca_extra_deduction = max(0, jubilee_ca_itemized - CA_STANDARD_DEDUCTION)
jubilee_ca_tax_savings_annual = jubilee_ca_extra_deduction * CA_TAX_RATE
jubilee_ca_tax_savings_monthly = jubilee_ca_tax_savings_annual / 12

print()
print(f"California State Tax Benefit:")
print(f"  Mortgage interest:              ${jubilee_annual_interest:,.0f}")
print(f"  Property tax:                   ${jubilee_annual_property_tax:,.0f}")
print(f"  State income tax:               ${jubilee_state_income_tax:,.0f}")
print(f"  Total itemized:                 ${jubilee_ca_itemized:,.0f}")
print(f"  vs Standard deduction:          ${CA_STANDARD_DEDUCTION:,.0f}")
print(f"  Extra deduction:                ${jubilee_ca_extra_deduction:,.0f}")
print(f"  Tax savings @ {CA_TAX_RATE*100:.1f}%:           ${jubilee_ca_tax_savings_annual:,.0f}/year")
print(f"  Monthly benefit:                ${jubilee_ca_tax_savings_monthly:,.0f}/month")

jubilee_total_tax_benefit_monthly = jubilee_federal_tax_savings_monthly + jubilee_ca_tax_savings_monthly
jubilee_aftertax_monthly = jubilee_pretax_monthly - jubilee_total_tax_benefit_monthly

print()
print(f"TOTAL TAX BENEFIT:                ${jubilee_total_tax_benefit_monthly:,.0f}/month")
print()
print(f"{'─' * 50}")
print(f"Pre-tax monthly cost:             ${jubilee_pretax_monthly:,.0f}")
print(f"Tax benefit:                      -${jubilee_total_tax_benefit_monthly:,.0f}")
print(f"AFTER-TAX MONTHLY COST:           ${jubilee_aftertax_monthly:,.0f}")
print()

# ============================================================================
# SCENARIO 2: TRADITIONAL 20% DOWN
# ============================================================================

print("=" * 95)
print("SCENARIO 2: TRADITIONAL 20% DOWN")
print("=" * 95)
print()

# Loan details
traditional_down_payment = HOME_PRICE * TRADITIONAL_DOWN_PCT
traditional_loan = HOME_PRICE - traditional_down_payment

# Monthly costs
traditional_mortgage = calculate_mortgage_payment(traditional_loan, CONVENTIONAL_RATE)
traditional_annual_property_tax = HOME_PRICE * PROPERTY_TAX_RATE
traditional_monthly_property_tax = traditional_annual_property_tax / 12
traditional_monthly_insurance = ANNUAL_INSURANCE / 12
traditional_annual_maintenance = HOME_PRICE * MAINTENANCE_RATE
traditional_monthly_maintenance = traditional_annual_maintenance / 12

traditional_pretax_monthly = (traditional_mortgage + traditional_monthly_property_tax +
                             traditional_monthly_insurance + traditional_monthly_maintenance)

# TAX BENEFITS
print("TAX DEDUCTION CALCULATION:")
print()

# Calculate first year mortgage interest
traditional_annual_interest = calculate_first_year_interest(traditional_loan, CONVENTIONAL_RATE)
print(f"  First year mortgage interest (full loan): ${traditional_annual_interest:,.0f}")

# Federal deductions (limited to interest on first $750k)
traditional_federal_mortgage_interest = calculate_first_year_interest(min(traditional_loan, MORTGAGE_DEBT_LIMIT),
                                                                      CONVENTIONAL_RATE)
print(f"  Deductible interest (first $750k):       ${traditional_federal_mortgage_interest:,.0f}")

traditional_federal_itemized = traditional_federal_mortgage_interest + FEDERAL_SALT_CAP
traditional_federal_extra_deduction = max(0, traditional_federal_itemized - FEDERAL_STANDARD_DEDUCTION)
traditional_federal_tax_savings_annual = traditional_federal_extra_deduction * FEDERAL_TAX_RATE
traditional_federal_tax_savings_monthly = traditional_federal_tax_savings_annual / 12

print()
print(f"Federal Tax Benefit:")
print(f"  Mortgage interest (deductible): ${traditional_federal_mortgage_interest:,.0f}")
print(f"  SALT deduction (capped):        ${FEDERAL_SALT_CAP:,.0f}")
print(f"  Total itemized:                 ${traditional_federal_itemized:,.0f}")
print(f"  vs Standard deduction:          ${FEDERAL_STANDARD_DEDUCTION:,.0f}")
print(f"  Extra deduction:                ${traditional_federal_extra_deduction:,.0f}")
print(f"  Tax savings @ {FEDERAL_TAX_RATE*100:.0f}%:         ${traditional_federal_tax_savings_annual:,.0f}/year")
print(f"  Monthly benefit:                ${traditional_federal_tax_savings_monthly:,.0f}/month")

# California deductions (no limit on mortgage interest, full SALT)
traditional_state_income_tax = TOTAL_SALT - traditional_annual_property_tax
traditional_ca_itemized = traditional_annual_interest + traditional_annual_property_tax + traditional_state_income_tax
traditional_ca_extra_deduction = max(0, traditional_ca_itemized - CA_STANDARD_DEDUCTION)
traditional_ca_tax_savings_annual = traditional_ca_extra_deduction * CA_TAX_RATE
traditional_ca_tax_savings_monthly = traditional_ca_tax_savings_annual / 12

print()
print(f"California State Tax Benefit:")
print(f"  Mortgage interest (full):       ${traditional_annual_interest:,.0f}")
print(f"  Property tax:                   ${traditional_annual_property_tax:,.0f}")
print(f"  State income tax:               ${traditional_state_income_tax:,.0f}")
print(f"  Total itemized:                 ${traditional_ca_itemized:,.0f}")
print(f"  vs Standard deduction:          ${CA_STANDARD_DEDUCTION:,.0f}")
print(f"  Extra deduction:                ${traditional_ca_extra_deduction:,.0f}")
print(f"  Tax savings @ {CA_TAX_RATE*100:.1f}%:           ${traditional_ca_tax_savings_annual:,.0f}/year")
print(f"  Monthly benefit:                ${traditional_ca_tax_savings_monthly:,.0f}/month")

traditional_total_tax_benefit_monthly = traditional_federal_tax_savings_monthly + traditional_ca_tax_savings_monthly
traditional_aftertax_monthly = traditional_pretax_monthly - traditional_total_tax_benefit_monthly

print()
print(f"TOTAL TAX BENEFIT:                ${traditional_total_tax_benefit_monthly:,.0f}/month")
print()
print(f"{'─' * 50}")
print(f"Pre-tax monthly cost:             ${traditional_pretax_monthly:,.0f}")
print(f"Tax benefit:                      -${traditional_total_tax_benefit_monthly:,.0f}")
print(f"AFTER-TAX MONTHLY COST:           ${traditional_aftertax_monthly:,.0f}")
print()

# ============================================================================
# SCENARIO 3: RENTING
# ============================================================================

print("=" * 95)
print("SCENARIO 3: RENTING")
print("=" * 95)
print()

renter_monthly_insurance = RENTERS_INSURANCE_ANNUAL / 12
renter_pretax_monthly = MONTHLY_RENT + renter_monthly_insurance

print("TAX DEDUCTION CALCULATION:")
print()
print(f"  No itemized deductions")
print(f"  Takes standard deduction")
print(f"  Tax benefit: $0/month")
print()

renter_aftertax_monthly = renter_pretax_monthly

print(f"{'─' * 50}")
print(f"Pre-tax monthly cost:             ${renter_pretax_monthly:,.0f}")
print(f"Tax benefit:                      -$0")
print(f"AFTER-TAX MONTHLY COST:           ${renter_aftertax_monthly:,.0f}")
print()

# ============================================================================
# COMPARISON TABLE
# ============================================================================

print("=" * 95)
print("SIDE-BY-SIDE COMPARISON")
print("=" * 95)
print()

print(f"{'Metric':<30} {'Jubilee':>18} {'20% Down':>18} {'Renting':>18}")
print("─" * 95)
print(f"{'Pre-tax monthly cost':<30} ${jubilee_pretax_monthly:>17,.0f} ${traditional_pretax_monthly:>17,.0f} ${renter_pretax_monthly:>17,.0f}")
print(f"{'Tax benefit':<30} -${jubilee_total_tax_benefit_monthly:>16,.0f} -${traditional_total_tax_benefit_monthly:>16,.0f} ${0:>17,.0f}")
print(f"{'AFTER-TAX monthly cost':<30} ${jubilee_aftertax_monthly:>17,.0f} ${traditional_aftertax_monthly:>17,.0f} ${renter_aftertax_monthly:>17,.0f}")
print()

# ============================================================================
# KEY INSIGHTS
# ============================================================================

print("=" * 95)
print("KEY INSIGHTS")
print("=" * 95)
print()

diff_jubilee_traditional = jubilee_aftertax_monthly - traditional_aftertax_monthly
diff_jubilee_rent = jubilee_aftertax_monthly - renter_aftertax_monthly
diff_traditional_rent = traditional_aftertax_monthly - renter_aftertax_monthly

print(f"1. AFTER-TAX MONTHLY COSTS:")
print(f"   Renting:     ${renter_aftertax_monthly:,.0f}/month (baseline)")
print(f"   Traditional: ${traditional_aftertax_monthly:,.0f}/month (+${diff_traditional_rent:,.0f} vs renting)")
print(f"   Jubilee:     ${jubilee_aftertax_monthly:,.0f}/month (+${diff_jubilee_rent:,.0f} vs renting)")
print()

if diff_jubilee_traditional > 0:
    print(f"2. JUBILEE vs TRADITIONAL:")
    print(f"   Jubilee costs ${diff_jubilee_traditional:,.0f}/month MORE after-tax")
    print(f"   Annual difference: ${diff_jubilee_traditional * 12:,.0f}/year")
else:
    print(f"2. TRADITIONAL vs JUBILEE:")
    print(f"   Traditional costs ${abs(diff_jubilee_traditional):,.0f}/month more after-tax")
    print(f"   Annual difference: ${abs(diff_jubilee_traditional) * 12:,.0f}/year")
print()

print(f"3. TAX BENEFITS MATTER:")
print(f"   Jubilee saves:     ${jubilee_total_tax_benefit_monthly:,.0f}/month in taxes")
print(f"   Traditional saves: ${traditional_total_tax_benefit_monthly:,.0f}/month in taxes")
print(f"   Traditional gets ${traditional_total_tax_benefit_monthly - jubilee_total_tax_benefit_monthly:,.0f}/month MORE in tax benefits")
print(f"   (Due to larger mortgage interest deduction)")
print()

print(f"4. THE COMPLETE PICTURE:")
print(f"   Traditional has:")
print(f"     • Lower pre-tax cost: ${traditional_pretax_monthly:,.0f} vs ${jubilee_pretax_monthly:,.0f}")
print(f"     • Larger tax benefit: ${traditional_total_tax_benefit_monthly:,.0f} vs ${jubilee_total_tax_benefit_monthly:,.0f}")
print(f"     • Lower after-tax cost: ${traditional_aftertax_monthly:,.0f} vs ${jubilee_aftertax_monthly:,.0f}")
print()
print(f"   Jubilee has:")
print(f"     • $370K more invested upfront")
print(f"     • But ${diff_jubilee_traditional:,.0f}/month higher after-tax cost")
print()

# ============================================================================
# CSV OUTPUT
# ============================================================================

print("=" * 95)
print("CSV DATA FOR CHART")
print("=" * 95)
print()
print("Scenario,Pre-Tax,Tax Benefit,After-Tax")
print(f"Jubilee,{jubilee_pretax_monthly:.0f},{jubilee_total_tax_benefit_monthly:.0f},{jubilee_aftertax_monthly:.0f}")
print(f"20% Down,{traditional_pretax_monthly:.0f},{traditional_total_tax_benefit_monthly:.0f},{traditional_aftertax_monthly:.0f}")
print(f"Renting,{renter_pretax_monthly:.0f},0,{renter_aftertax_monthly:.0f}")
print()

print("=" * 95)
print("TAX ASSUMPTIONS")
print("=" * 95)
print()
print(f"Filing status: Married Filing Jointly")
print(f"Federal tax rate: {FEDERAL_TAX_RATE*100:.0f}%")
print(f"CA tax rate: {CA_TAX_RATE*100:.1f}%")
print(f"Federal standard deduction: ${FEDERAL_STANDARD_DEDUCTION:,.0f}")
print(f"CA standard deduction: ${CA_STANDARD_DEDUCTION:,.0f}")
print(f"Total SALT (state + property tax): ${TOTAL_SALT:,.0f}")
print(f"Federal SALT cap: ${FEDERAL_SALT_CAP:,.0f}")
print(f"Mortgage debt limit (federal): ${MORTGAGE_DEBT_LIMIT:,.0f}")
print()
