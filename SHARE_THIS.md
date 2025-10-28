# HYSA vs Stocks: Capital Gains Tax Analysis

## Quick Summary

**Question:** To save $410,000 over 5 years, should you use HYSA (avoid cap gains tax) or stocks (pay cap gains tax)?

**Answer:** Use stocks. Even after paying $16,794 in capital gains tax, you come out ahead because you only need to contribute $357,684 vs $380,530 with HYSA.

**Conclusion:** You pay **$22,846 MORE** to avoid **$16,794 in tax** (1.36x more expensive).

---

## How to Verify the Math

### Requirements
- Python 3 (any version)

### Run the Calculation

```bash
python3 hysa_vs_stocks_simple.py
```

### Expected Output

```
HYSA monthly:         $6,342.16
Stock monthly:        $5,961.40
HYSA needs MORE:      $380.77/month (6.4% more)

HYSA total contrib:   $380,529.79
Stock total contrib:  $357,683.81
HYSA needs MORE:      $22,845.98 total

HYSA tax paid:        $0.00
Stock tax paid:       $16,793.70
```

---

## Key Assumptions

### HYSA (3% after-tax)
- Nominal rate: 4.5%
- Taxed yearly at 41.3% (Fed + CA ordinary income)
- After-tax growth: **3.0%**
- No capital gains tax when withdrawing

### Stocks (7% growth)
- Growth rate: 7%
- Tax deferred until sale
- Capital gains tax: **24.3%** (15% Fed + 9.3% CA)

---

## The Math

### HYSA Approach
To reach $410,000 at 3% annual return over 60 months:
- Monthly contribution = $6,342.16
- Total contributed = $380,529.79
- Interest earned = $29,470.21 (already taxed yearly)
- Available = $410,000.00

### Stocks Approach
Need to end with $410,000 AFTER capital gains tax:
- Target before tax = $426,793.70
- Monthly contribution = $5,961.40
- Total contributed = $357,683.81
- Capital gains = $69,109.89
- Tax (24.3%) = $16,793.70
- Available = $410,000.00

### Verdict
- HYSA requires $22,845.98 MORE in contributions
- Stocks requires $16,793.70 in tax
- Net: You pay 1.36x more to avoid the tax

---

## Why This Happens

**Tax drag vs tax payment:**
- HYSA: Taxed EVERY YEAR at 41.3% (slow growth)
- Stocks: Taxed ONCE at sale at 24.3% (fast growth, then tax)

The opportunity cost of slow growth exceeds the one-time tax payment.

---

## Files

- **hysa_vs_stocks_simple.py** - Clean, standalone calculation (80 lines, well-commented)
- **hysa_vs_stocks_capital_gains.py** - Detailed analysis with Jubilee scenarios

---

## Share This Calculation

1. **GitHub Gist**: Copy `hysa_vs_stocks_simple.py` to https://gist.github.com/
2. **Google Colab**: Upload and run in browser (no installation needed)
3. **Direct Link**: Share this repo: https://github.com/njayant12/rent-vs-buy

---

## Questions?

The calculation uses the standard future value of annuity formula:
```
FV = PMT × [(1 + r)^n - 1] / r
```

Where:
- PMT = monthly payment
- r = monthly interest rate
- n = number of months

We solve for PMT given FV (target amount).
