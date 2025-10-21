# Year 1 & 2 Debug Summary: Rent vs Buy with 20% Down

## Setup
- **Starting Capital**: $410,000
- **Property Price**: $1.9M
- **Rent**: $5,800/month (3% annual growth)
- **Home Appreciation**: 3%
- **Investment Return**: 7%
- **Constraint**: Monthly income matched to 3% down baseline ($14,783/month)

## Key Finding: Cash Flow Makes All the Difference

### Monthly Cash Flow Comparison
| Scenario | Monthly Cost | Monthly Savings vs 3% Down | Annual Savings to Invest |
|----------|-------------|----------------------------|-------------------------|
| 3% Down (baseline) | $14,783 | $0 | $0 |
| 20% Down | $11,263 | $3,520 | $42,239 |
| Renting | $5,800 | $8,983 | $107,797 |

**Why 20% down saves money monthly:**
- No PMI ($1,583/month saved!)
- Smaller loan = lower mortgage payment

---

## Year 1 Breakdown

### 20% Down Buying

| Component | Amount | Notes |
|-----------|--------|-------|
| **GAINS** | | |
| Home Appreciation (3%) | +$57,000 | Property: $1.9M → $1.957M |
| Home Equity (principal) | +$18,666 | Mortgage paid down |
| Investment Returns | +$1,478 | On $42,239 saved monthly (half-year avg) |
| **COSTS** | | |
| Net Costs (after tax) | -$125,556 | Mortgage + tax + insurance - tax benefit |
| Closing Costs | -$30,000 | One-time upfront |
| **NET YEAR 1** | **-$78,412** | |

**Tax Benefit Details:**
- Mortgage interest paid: $90,692
- Property tax: $22,800
- Tax savings: $9,602 (from itemizing vs standard deduction)

**Investment Balance End of Year 1**: $43,717

---

### Renting

| Component | Amount | Notes |
|-----------|--------|-------|
| **GAINS** | | |
| Investment Returns | +$32,473 | $28,700 on starting $410K + $3,773 on monthly flow |
| **COSTS** | | |
| Rent Paid | -$69,600 | $5,800/month |
| **NET YEAR 1** | **-$37,127** | |

**Investment Balance End of Year 1**: $550,269

**Year 1 Winner: Renting** (by $41,285)

---

## Year 2 Breakdown

### 20% Down Buying

| Component | Amount | Notes |
|-----------|--------|-------|
| **GAINS** | | |
| Home Appreciation (3%) | +$58,710 | Property: $1.957M → $2.016M |
| Home Equity (principal) | +$19,817 | Cumulative principal: $38,483 |
| Investment Returns | +$4,539 | On growing investment balance |
| **COSTS** | | |
| Net Costs (after tax) | -$126,110 | (Property tax up 2%, insurance up 3%) |
| **NET YEAR 2** | **-$43,044** | |

**Investment Balance End of Year 2**: $90,494
**Home Equity End of Year 2**: $534,193

---

### Renting

| Component | Amount | Notes |
|-----------|--------|-------|
| **GAINS** | | |
| Investment Returns | +$42,292 | $38,519 on $550K + $3,773 on monthly flow |
| **COSTS** | | |
| Rent Paid | -$71,688 | $5,974/month (up 3%) |
| **NET YEAR 2** | **-$29,396** | |

**Investment Balance End of Year 2**: $700,358

**Year 2 Winner: Renting** (by $13,648)

---

## Cumulative 2-Year Results

| Metric | Renting | 20% Down Buying | Difference |
|--------|---------|-----------------|------------|
| **Cumulative Net Position** | -$66,523 | -$121,456 | Rent wins by $54,933 |
| | | | |
| **Total Net Worth** | | | |
| Investments | $700,358 | $90,494 | |
| Home Equity | $0 | $534,193 | |
| **Total Net Worth** | **$700,358** | **$624,687** | Rent wins by $75,671 |

---

## Key Insights

### 1. **Investment Compounding is Powerful**
- Renter starts with full $410K invested
- Buyer starts with $0 invested (all spent on down + closing)
- Renter's $410K grows to $700K in 2 years
- Buyer's investment balance only reaches $90K

### 2. **Monthly Cash Flow Advantage Compounds**
- Renter saves $8,983/month vs baseline
- 20% down saves only $3,520/month vs baseline
- Renter invests 2.5x more cash each month

### 3. **Home Appreciation Alone Isn't Enough at 3%**
- Total home appreciation over 2 years: $115,710
- Total equity from principal paydown: $38,483
- **Total home value creation: $154,193**
- But renter's investment grew by **$290,358**
- Difference: $136,165 in favor of renting

### 4. **The Crossover Point**
At 3% appreciation, renting wins. But what if appreciation was 7%?

**Year 1 with 7% appreciation (hypothetical):**
- Home appreciation: $133,000 (instead of $57,000)
- Additional $76,000 in gains
- This would swing year 1 from -$78,412 to -$2,412
- And renting would still win year 1 (but barely)

### 5. **Net Position vs Net Worth**
Both scenarios show negative net positions (spending more than gaining), but:
- Renter maintains higher liquidity ($700K cash)
- Buyer has illiquid equity ($534K) + some cash ($90K)
- Renter has more flexibility for other investments, emergencies, or opportunities

---

## Debug Notes

### Split Verification
✓ **Home Appreciation**: Correctly split out (property value growth)
✓ **Home Equity**: Correctly shows principal paydown only
✓ **Investment Returns**: Properly calculated with:
  - Return on starting balance
  - Return on monthly cash flow (using half-year average)
  - Compounding year over year

### Tax Calculation Verification
✓ Mortgage interest deductible on first $750K of debt
✓ SALT cap at $10K applied correctly
✓ Tax savings = (itemized - standard) × 41.3% tax rate

### Cash Flow Matching Verification
✓ All scenarios use same baseline monthly income ($14,783)
✓ Savings properly invested at 7% return
✓ Monthly contributions tracked separately from starting balance

---

## Next Steps for 30-Year Projection

To extend this to 30 years, we need to track:
1. **Home appreciation** compounding at 3% annually
2. **Principal paydown** accelerating each year
3. **Investment balance** growing from monthly contributions + returns
4. **Costs** inflating (property tax 2%, insurance 3%, rent 3%)
5. **Tax benefits** changing as mortgage interest decreases
6. **Break-even point** where buying surpasses renting

Key question: At what appreciation rate does buying catch up?
- 3% appreciation: Renting wins
- 5% appreciation: TBD
- 7% appreciation: Buying likely wins
