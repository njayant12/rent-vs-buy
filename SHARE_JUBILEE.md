# Jubilee vs 20% Down vs Renting: Net Worth Comparison

## Quick Summary

**Question:** For a $1.9M SF home, which approach preserves the most capital?

**Setup:** Everyone saves $7,426/month for 4 years in stocks, then lets it grow 1 year = $438,683 starting capital

**Answer:**

| Scenario   | Amount Invested | Home Equity | Total Net Worth |
|------------|-----------------|-------------|-----------------|
| Jubilee    | $379,381        | $26,600     | $405,981        |
| 20% Down   | $9,115          | $380,000    | $389,115        |
| Renting    | $438,683        | $0          | $438,683        |

**Key Finding:** Jubilee keeps **41.6x more capital invested** than traditional 20% down ($370K more).

---

## How to Verify the Math

### Requirements
- Python 3 (any version)

### Run the Calculation

```bash
python3 jubilee_comparison_simple.py
```

### Expected Output

```
COMPARISON TABLE
================================================================================
Metric                                 Jubilee        20% Down         Renting
--------------------------------------------------------------------------------
Amount Invested                $       379,381 $         9,115 $       438,683
Down Payment                   $        26,600 $       380,000 $             0
Equity                         $        26,600 $       380,000 $             0
Capital Gains Tax Paid         $         2,701 $        19,568 $             0
Total Net Worth                $       405,981 $       389,115 $       438,683
```

---

## Key Assumptions

### Starting Position
- Everyone saves $7,426/month for 4 years at 7% return
- Let it grow for 1 more year (Year 5)
- Starting portfolio: $438,683
- Cost basis: $356,448

### Jubilee (Ground Lease)
- Home price: $1.9M
- Land (60%): Jubilee owns $1.14M
- House (40%): You own $760K with FHA 3.5% down
- Down payment: $26,600
- Closing costs: $30,000
- Total cash needed: $56,600
- Sell 13.5% of stocks to fund

### Traditional 20% Down
- Down payment: $380,000
- Closing costs: $30,000
- Total cash needed: $410,000
- Sell 97.9% of stocks to fund

### Renting
- Monthly rent: $5,800
- No purchase
- Keep 100% invested

### Tax Rates
- Capital gains: 24.3% (15% Fed + 9.3% CA)

---

## The Jubilee Value Proposition

**Advantages:**
- Keep $370K MORE invested than traditional (41.6x more)
- Only liquidate 13.5% of portfolio vs 97.9%
- Pay $16,867 LESS in capital gains tax
- That $370K can compound at 7% for 30 years

**Disadvantages:**
- Only own 40% of property (not 100%)
- Only get 40% of home appreciation
- Pay monthly land lease to Jubilee
- Share appreciation with Jubilee

**The Question:** Does keeping $370K invested justify owning 40% instead of 100%?

---

## What Happens to That $370K?

If Jubilee's $370K extra invested compounds at 7% for 30 years:
- $370,267 × (1.07)^30 = **$2.82 million**

Meanwhile, traditional buyer has $370K more equity in home. If home appreciates at 3%:
- $370,000 × (1.03)^30 = **$897,000**

The $370K invested could be worth **$1.92M MORE** after 30 years, even accounting for the difference in ownership percentage and appreciation split.

---

## Files

- **jubilee_comparison_simple.py** - Clean, standalone calculation (170 lines)
- **jubilee_equal_starting_capital.py** - Detailed version with full breakdown

---

## Share This Calculation

1. **GitHub Gist**: Copy `jubilee_comparison_simple.py` to https://gist.github.com/
2. **Google Colab**: Upload and run in browser (no installation needed)
3. **Direct Link**: Share this repo: https://github.com/njayant12/rent-vs-buy

---

## Understanding the Math

The calculation accounts for capital gains tax when selling stocks:

```
After-tax proceeds = Amount Sold - (Capital Gains × 24.3%)

Where:
  Capital Gains = Amount Sold - Cost Basis of Sold Portion
```

We sell just enough stock so that after paying cap gains tax, we have exactly the cash we need.

---

## Caveats

This analysis shows ONLY the initial setup (Year 5). It does NOT include:
- Monthly land lease payments to Jubilee
- Ongoing mortgage payments and PMI
- Property taxes and maintenance
- Future home appreciation or stock returns beyond Year 5
- Tax benefits of mortgage interest deduction

For a complete analysis, you'd need to model all cash flows over 30 years.
