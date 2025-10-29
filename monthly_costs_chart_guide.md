# Stacked Bar Chart Guide: Monthly Costs Comparison

## Chart Data

Use the data from `monthly_costs_chart_data.csv`

## Recommended Visualization

### Stacked Bar Chart Layout

**X-axis:** Three bars (Jubilee, 20% Down, Renting)

**Y-axis:** Monthly cost in dollars ($0 - $15,000)

**Stacks (bottom to top):**

#### Jubilee Bar ($14,208 total):
1. Mortgage (blue): $4,595
2. PMI (orange): $336
3. Land Lease (red): $5,700 ← **Most distinctive**
4. Property Tax (purple): $1,868
5. Insurance (green): $125
6. Maintenance (yellow): $1,583

#### 20% Down Bar ($12,837 total):
1. Mortgage (blue): $9,260 ← **Tallest segment**
2. PMI (orange): $0
3. Land Lease (red): $0
4. Property Tax (purple): $1,868
5. Insurance (green): $125
6. Maintenance (yellow): $1,583

#### Renting Bar ($5,817 total):
1. Rent (gray): $5,800 ← **Simple bar**
2. Insurance (green): $17

---

## Color Scheme Recommendations

```
Mortgage:      #2563eb (Blue)       - Traditional housing cost
PMI:           #f97316 (Orange)     - Extra FHA cost
Land Lease:    #dc2626 (Red)        - Jubilee unique cost
Property Tax:  #9333ea (Purple)     - Government obligation
Insurance:     #16a34a (Green)      - Protection
Maintenance:   #eab308 (Yellow)     - Upkeep
Rent:          #64748b (Gray)       - Renting cost
```

---

## Key Annotations to Add

### On Jubilee Bar:
- Arrow pointing to Land Lease segment: "**$5,700/mo to Jubilee**"
- Total label: "$14,208/mo"

### On 20% Down Bar:
- Arrow pointing to Mortgage segment: "**$9,260/mo mortgage**"
- Total label: "$12,837/mo (lowest ownership cost)"

### On Renting Bar:
- Total label: "$5,817/mo (lowest overall)"

### Chart Title:
"**First Year Average Monthly Costs: $1.9M SF Home**"

### Chart Subtitle:
"Jubilee costs $1,371/mo more than traditional despite lower mortgage"

---

## Alternative: Side-by-Side Component Bars

Instead of stacked, show each component as a separate grouped bar for easier comparison:

**Component Groups:**
1. Mortgage: [Jubilee: $4,595] [Traditional: $9,260] [Renting: $0]
2. Land Lease: [Jubilee: $5,700] [Traditional: $0] [Renting: $0]
3. Other Costs: [Jubilee: $3,913] [Traditional: $3,577] [Renting: $17]

This makes the land lease stand out more clearly.

---

## Key Insight to Highlight

**Visual Story:**
- Renting bar is shortest (obvious savings)
- Traditional bar is middle height (moderate monthly cost)
- Jubilee bar is TALLEST (surprising!)

**The Surprise:**
Most people expect Jubilee to be cheaper monthly. The chart shows it's actually **$1,371/mo more expensive** due to the land lease.

**The Value Proposition:**
Jubilee's advantage isn't monthly cost - it's **capital preservation** ($370K more invested).

---

## Quick Excel/Google Sheets Instructions

### Create Stacked Bar Chart:

1. Import `monthly_costs_chart_data.csv`
2. Select columns B-H (Mortgage through Rent)
3. Insert → Chart → Stacked Column Chart
4. Set rows as data series (each scenario is a bar)
5. Format colors as suggested above
6. Add data labels showing segment values
7. Add total labels at top of each bar

### For Simpler View (3-Component Chart):

Create a simplified version with just:
- Housing Payment (Mortgage for traditional, Mortgage+Land Lease for Jubilee, Rent for renting)
- Taxes & Insurance
- Maintenance

This makes comparison easier for presentations.

---

## Data Summary for Chart

```
Monthly Housing Payment:
  Renting:     $5,800 (rent)
  Jubilee:     $10,631 (mortgage + PMI + land lease)
  Traditional: $9,260 (mortgage only)

Taxes & Insurance:
  Renting:     $17
  Jubilee:     $1,993
  Traditional: $1,993

Maintenance:
  Renting:     $0
  Jubilee:     $1,583
  Traditional: $1,583

TOTAL:
  Renting:     $5,817
  Jubilee:     $14,208
  Traditional: $12,837
```

---

## Talking Points

When presenting this chart:

1. **"Renting is cheapest monthly"** - No surprise at $5,817/mo

2. **"Traditional 20% down costs $12,837/mo"** - Standard ownership costs

3. **"Jubilee costs $14,208/mo - $1,371 MORE than traditional"** - This surprises people!

4. **"Why? The $5,700/mo land lease"** - Point to the red segment

5. **"But remember: Jubilee keeps $370K more invested"** - That compounds to $2.82M over 30 years

6. **"Monthly cost vs capital preservation"** - The core trade-off

---

## Chart Variants

### Variant 1: Annual Costs
Multiply all monthly numbers by 12:
- Renting: $69,800/year
- Jubilee: $170,490/year
- Traditional: $154,043/year

### Variant 2: 30-Year Total
Show cumulative cost over 30 years (without factoring in appreciation or investment returns):
- Renting: $2.09M
- Jubilee: $5.11M
- Traditional: $4.62M

*(But this is misleading without accounting for equity and appreciation)*

---

## Files

- **monthly_costs_chart_data.csv** - Ready to import
- **monthly_costs_analysis.py** - Full calculation script
- **monthly_costs_quality_check.md** - Detailed verification of all assumptions
