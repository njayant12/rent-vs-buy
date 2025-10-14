# Rent vs. Buy Calculator with Tax Benefits - Project Specification

## Overview
A comprehensive rent vs. buy calculator that helps users make informed housing decisions by comparing the true costs of renting vs. buying over time, including detailed tax benefit analysis from mortgage interest deduction, property tax deduction, and capital gains exclusion for primary residences.

## Requirements

### Core Functionality
1. **Scenario Comparison**: Compare renting vs. buying for the same property over time (5, 10, 15, 20, 25, 30 years)
2. **Tax Benefit Analysis**: Calculate mortgage interest deduction, SALT deduction, and capital gains exclusion
3. **Real-time Calculations**: Update results as user types
4. **Multiple Scenarios**: Support different down payments (3%, 20%, 100%) and interest rates (5%, 6%)
5. **Location Presets**: Quick-select for SF, Redwood City, Palo Alto with typical prices
6. **Clear Results Display**: Show total cost comparison, tax savings, and break-even point
7. **Responsive Design**: Work seamlessly on desktop, tablet, and mobile

### Input Fields

#### Property Information
- **Purchase Price** (currency, e.g., $1,900,000)
- **Monthly Rent** (currency, e.g., $5,800)
- **Location Preset** (optional quick-select: San Francisco, Redwood City, Palo Alto)

#### Financing Options
- **Down Payment Percentage** (3%, 20%, or 100%)
- **Interest Rate** (5% optimistic, 6% conservative)
- **Loan Term** (fixed at 30 years)

#### Tax Information
- **Filing Status** (Single or Married)
- **W-2 Income** (annual gross income)
- **Federal Tax Bracket** (percentage)
- **State Tax Rate** (percentage, e.g., 9.3% for CA)
- **State Income Tax Paid** (annual, for SALT deduction)

#### Fixed Assumptions (Pre-populated, user can modify)
- **Property Tax Rate**: 1.2% of purchase price annually
- **Homeowners Insurance**: $3,000/year
- **Renters Insurance**: $200/year
- **PMI Rate**: 1% of purchase price annually (when down payment < 20%)
- **Buying Closing Costs**: $30,000
- **Selling Closing Costs**: $30,000 + 6% commission
- **Property Appreciation Rate**: 3% (conservative) or 7% (optimistic)
- **General Inflation Rate**: 3% annually (for rent and expenses)
- **Property Tax Increase**: 2% annually

#### Major Maintenance Costs (Inflation-adjusted)
- **Roof Replacement**: $25,000 every 25 years
- **Water Heater Replacement**: $3,000 every 10 years
- **Flooring Replacement**: $10,000 every 10 years

### Output Metrics

#### Summary Comparison (After 30 years or selected timeframe)
1. **Total Cost of Renting** vs **Total Cost of Buying** (Net Present Value)
2. **Break-even Point** (Year when buying becomes cheaper than renting)
3. **Net Worth Difference** (Equity gained from buying vs. invested savings from renting)
4. **Total Tax Savings from Homeownership** (Cumulative over timeframe)

#### Annual Breakdown (Year-by-year table)
- Year
- Rent paid (with 3% inflation)
- Mortgage payment (P&I)
- Property taxes
- Insurance
- Maintenance costs
- PMI (if applicable)
- Annual tax benefit (itemized deductions vs. standard)
- Net tax savings
- Property value (with appreciation)
- Remaining mortgage balance
- Home equity
- Cumulative cost (rent vs. buy)

#### Tax Benefit Details (First Year Example)
1. **Mortgage Interest Paid** (capped at interest on $750K of debt)
2. **Property Taxes Paid**
3. **State Income Tax Paid**
4. **Total SALT Deduction** (Property tax + State income tax, capped at $10,000)
5. **Total Itemized Deductions** (Mortgage interest + SALT)
6. **Standard Deduction** (for comparison)
7. **Excess Deductions** (Itemized - Standard)
8. **Net Tax Savings** (Excess × Effective tax rate)

#### Capital Gains Analysis (At Sale)
- **Purchase Price**
- **Sale Price** (after appreciation)
- **Total Capital Gain**
- **Capital Gains Exclusion** ($250K single, $500K married)
- **Taxable Capital Gain** (if any)
- **Capital Gains Tax Owed** (if any)

### Output Format
- Dashboard layout with key metrics prominently displayed
- Color coding:
  - Green for positive cash flow
  - Yellow for break-even
  - Red for negative cash flow
- Clear labels with tooltips explaining each metric
- Monthly and annual breakdowns
- Visual progress indicators or charts

## Tech Stack

### Frontend
- **Framework**: React 18+ with Vite for fast development
- **Styling**: Tailwind CSS for utility-first responsive design
- **State Management**: React hooks (useState, useEffect)
- **Form Handling**: Controlled components with validation
- **Charts**: Chart.js or Recharts for visual data representation

### Storage
- **LocalStorage**: Save calculation history and user preferences

### Development Tools
- **Package Manager**: npm
- **Version Control**: Git + GitHub
- **Code Editor**: Any modern editor (VS Code recommended)

## Design Guidelines

### Layout
- Single-page application with clear sections
- Left/top panel: Input form
- Right/bottom panel: Results dashboard
- Responsive breakpoints for mobile, tablet, desktop

### Visual Design
- Clean, professional appearance
- Generous whitespace
- Clear typography hierarchy
- Consistent color scheme:
  - Primary: Blue (#3B82F6)
  - Success: Green (#10B981)
  - Warning: Yellow (#F59E0B)
  - Danger: Red (#EF4444)
  - Neutral: Gray (#6B7280)

### User Experience
- Real-time calculation updates (debounced for performance)
- Clear input labels with helper text
- Tooltips for technical terms
- Input validation with error messages
- Mobile-friendly touch targets
- Keyboard navigation support

### Accessibility
- Semantic HTML
- ARIA labels where needed
- Keyboard accessible
- Screen reader friendly
- Sufficient color contrast

## Milestones

### Milestone 1: UI Setup with Dummy Data
**Goal**: Create the complete user interface with hardcoded sample results

**Tasks**:
1. Initialize React + Vite project
2. Install dependencies (Tailwind CSS, React Icons)
3. Create project structure (components, utils, styles)
4. Build input form component with all fields
5. Create results dashboard component with hardcoded data
6. Add responsive layout
7. Style with Tailwind CSS
8. Test on localhost
9. Verify mobile responsiveness

**Success Criteria**:
- All input fields render correctly
- Results display with sample data
- Layout is responsive
- App runs without errors on localhost

### Milestone 2: Implement Real Calculations
**Goal**: Connect inputs to actual financial calculations

**Tasks**:
1. Create calculation utility functions:
   - `calculateMortgage()` - Monthly payment formula
   - `calculateCashFlow()` - Income minus expenses
   - `calculateROI()` - Return on investment metrics
   - `calculateCapRate()` - Capitalization rate
   - `calculateBreakEven()` - Months to recover investment
2. Implement React state management for all inputs
3. Connect inputs to calculation functions
4. Update results display with real calculations
5. Add input validation (min/max, required fields)
6. Handle edge cases (zero values, negative numbers)
7. Add debouncing for performance (300ms delay)
8. Format currency and percentage outputs
9. Test all calculations with various scenarios

**Success Criteria**:
- All calculations are mathematically accurate
- Results update in real-time as user types
- Input validation works correctly
- No errors with edge cases
- Currency formatting is consistent

### Milestone 3: Enhanced Features
**Goal**: Add advanced functionality and polish

**Tasks**:
1. Add "Save Calculation" feature (localStorage)
2. Create calculation history viewer
3. Implement "Compare Properties" tool (side-by-side)
4. Add amortization schedule table
5. Create export functionality (CSV or PDF)
6. Add print-friendly stylesheet
7. Implement data visualization (charts for cash flow projection)
8. Add dark mode toggle
9. Create help/info modal with calculation explanations
10. Performance optimization
11. Cross-browser testing
12. Final mobile testing and polish

**Success Criteria**:
- Users can save and reload calculations
- Comparison tool works with 2-3 properties
- Export functions correctly
- Charts display properly
- App is performant and polished

## Calculation Formulas

### Monthly Mortgage Payment
```
M = P * [r(1+r)^n] / [(1+r)^n-1]

Where:
M = Monthly payment (Principal + Interest only)
P = Loan principal (purchase price - down payment)
r = Monthly interest rate (annual rate / 12 / 100)
n = Number of payments (years * 12) = 360 for 30-year loan
```

### Annual Mortgage Interest Paid
```
For each year, calculate based on amortization schedule:
- Start with remaining balance from previous year
- Calculate interest portion of each monthly payment
- Sum 12 months of interest

For tax purposes:
- Interest is deductible on first $750K of mortgage debt
- If mortgage > $750K, prorate: (750000 / mortgage_amount) × total_interest
```

### Property Taxes (Annual)
```
Year 1: Purchase Price × 1.2%
Year N: Previous Year Tax × 1.02 (2% annual increase)
```

### PMI (Private Mortgage Insurance)
```
If down payment < 20%:
  Annual PMI = Purchase Price × 1%
  Monthly PMI = Annual PMI / 12

PMI stops when equity reaches 20% of original purchase price
```

### Total Monthly Cost of Ownership
```
Year 1:
  Mortgage P&I +
  Property Tax / 12 +
  Homeowners Insurance / 12 +
  PMI (if applicable) / 12 +
  Maintenance costs / 12

Maintenance costs include amortized major replacements:
  - Roof: $25,000 / 25 years = $1,000/year
  - Water heater: $3,000 / 10 years = $300/year
  - Flooring: $10,000 / 10 years = $1,000/year
  - All adjusted for inflation at 3% annually
```

### Tax Benefit Calculation (Annual)

#### Step 1: Calculate Itemized Deductions
```
Mortgage Interest = (calculated from amortization, capped at $750K debt)
Property Tax Paid = (annual property tax)
State Income Tax Paid = (user input)

SALT Deduction = MIN(Property Tax + State Income Tax, $10,000)
Total Itemized Deductions = Mortgage Interest + SALT Deduction
```

#### Step 2: Compare to Standard Deduction
```
Standard Deduction (2025):
  Single: $15,000
  Married: $31,500

Excess Deductions = MAX(0, Itemized - Standard)
```

#### Step 3: Calculate Tax Savings
```
Combined Tax Rate = Federal Rate + State Rate
Net Tax Savings = Excess Deductions × Combined Tax Rate
```

#### Example (from user's scenario):
```
Married couple, $400K income, $2M home, 20% down ($1.6M mortgage at 6%)

Year 1 Mortgage Interest: $96,000
Interest deductible (capped at $750K): $96,000 × (750,000/1,600,000) = $45,000
Property Tax: $24,000
State Income Tax: $30,000
SALT Deduction: MIN($24,000 + $30,000, $10,000) = $10,000

Total Itemized: $45,000 + $10,000 = $55,000
Standard Deduction: $31,500
Excess: $55,000 - $31,500 = $23,500
Combined Rate: 32% + 9.3% = 41.3%
Tax Savings: $23,500 × 41.3% = $9,706
```

### Capital Gains at Sale
```
Purchase Price: Original price
Sale Price: Purchase Price × (1 + appreciation_rate)^years
Total Capital Gain: Sale Price - Purchase Price

Capital Gains Exclusion:
  Single: $250,000
  Married: $500,000

Taxable Gain: MAX(0, Total Gain - Exclusion)
Capital Gains Tax: Taxable Gain × 20% (long-term rate for high earners)
```

### Net Proceeds from Sale
```
Sale Price
- Remaining Mortgage Balance
- Selling Closing Costs ($30,000)
- Selling Commission (6% of Sale Price)
- Capital Gains Tax (if any)
= Net Proceeds to Seller
```

### Total Cost of Buying (30-year analysis)
```
Down Payment
+ Buying Closing Costs ($30,000)
+ Sum of all mortgage payments (30 years)
+ Sum of all property taxes (with 2% increases)
+ Sum of all insurance payments (with 3% inflation)
+ Sum of all maintenance costs (with 3% inflation)
+ PMI payments (until 20% equity)
- Tax savings (annual, summed over all years)
- Net proceeds from sale (at end of period)
= Total Cost of Buying
```

### Total Cost of Renting (30-year analysis)
```
Sum of all rent payments over 30 years
  Year 1: Monthly Rent × 12
  Year N: Previous Year Rent × 1.03
+ Renters Insurance × 30 years (with 3% inflation)
= Total Cost of Renting
```

### Break-even Analysis
```
For each year 1-30:
  Calculate cumulative cost of renting
  Calculate cumulative cost of buying (including opportunity cost)

Break-even year = First year where buying becomes cheaper than renting
```

### Property Value Growth
```
Year N Property Value = Purchase Price × (1 + appreciation_rate)^N

Where appreciation_rate is:
  3% (conservative/national average)
  7% (optimistic/Cupertino 2000-2025)
```

### Home Equity
```
Year N Equity = Year N Property Value - Remaining Mortgage Balance
```

## Location Presets

Pre-populate with typical Bay Area prices (user can modify):

```javascript
const LOCATION_PRESETS = {
  'San Francisco (Bernal Heights)': {
    purchasePrice: 1900000,
    monthlyRent: 5800,
  },
  'Redwood City': {
    purchasePrice: 2200000,
    monthlyRent: 6000,
  },
  'Palo Alto': {
    purchasePrice: 3200000,
    monthlyRent: 8000,
  },
  'Custom': {
    purchasePrice: 0,
    monthlyRent: 0,
  }
};
```

## Default Assumptions

These should be pre-filled but user-editable:

```javascript
const DEFAULT_ASSUMPTIONS = {
  propertyTaxRate: 1.2,           // % of purchase price
  homeownersInsurance: 3000,      // annual
  rentersInsurance: 200,          // annual
  pmiRate: 1.0,                   // % of purchase price when down < 20%
  buyingClosingCosts: 30000,      // flat fee
  sellingClosingCosts: 30000,     // flat fee
  sellingCommission: 6.0,         // % of sale price

  // Appreciation and inflation
  appreciationRate: 3,            // % annual (can toggle 3% or 7%)
  rentInflationRate: 3,           // % annual
  generalInflationRate: 3,        // % annual for expenses
  propertyTaxIncreaseRate: 2,     // % annual

  // Major maintenance (all inflation-adjusted)
  roofReplacement: {
    cost: 25000,
    frequency: 25  // years
  },
  waterHeaterReplacement: {
    cost: 3000,
    frequency: 10
  },
  flooringReplacement: {
    cost: 10000,
    frequency: 10
  },

  // Tax constants (2025)
  mortgageInterestCap: 750000,    // max debt for interest deduction
  saltCap: 10000,                 // SALT deduction cap
  standardDeduction: {
    single: 15000,
    married: 31500
  },
  capitalGainsExclusion: {
    single: 250000,
    married: 500000
  }
};
```

## File Structure
```
real-estate-calculator/
├── src/
│   ├── components/
│   │   ├── InputForm.jsx              # Main input form
│   │   ├── LocationPresets.jsx        # Location quick-select buttons
│   │   ├── TaxInputs.jsx              # Tax-related inputs
│   │   ├── AssumptionsPanel.jsx       # Advanced assumptions (collapsible)
│   │   ├── ResultsSummary.jsx         # Top-level comparison
│   │   ├── TaxBenefitsCard.jsx        # Tax savings breakdown
│   │   ├── AnnualTable.jsx            # Year-by-year breakdown
│   │   ├── CapitalGainsCard.jsx       # Sale proceeds analysis
│   │   ├── MetricCard.jsx             # Reusable metric display
│   │   └── BreakEvenChart.jsx         # Visual break-even analysis
│   ├── utils/
│   │   ├── mortgageCalculations.js    # Mortgage, amortization, PMI
│   │   ├── taxCalculations.js         # Tax benefits, deductions
│   │   ├── rentVsBuyCalculations.js   # Total cost comparisons
│   │   ├── formatters.js              # Currency, percentage formatting
│   │   ├── validation.js              # Input validation
│   │   └── constants.js               # Location presets, defaults
│   ├── hooks/
│   │   └── useRentVsBuy.js           # Main state management hook
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── public/
├── spec.md
├── todo.md
├── .claude.md
├── package.json
├── vite.config.js
├── tailwind.config.js
└── README.md
```

## Success Metrics
- All calculations are accurate to 2 decimal places
- Tax calculations match the example scenario provided
- Page loads in under 2 seconds
- Works on Chrome, Firefox, Safari, Edge
- Mobile responsive (320px - 1920px)
- No console errors or warnings
- Passes basic accessibility audit
- Year-by-year table displays correctly for 30 years

## Important Disclaimers

**MUST display prominently in the app:**

```
⚠️ EDUCATIONAL PURPOSE ONLY ⚠️

This calculator is for education and entertainment purposes only
and is NOT financial advice.

I am not a financial professional, tax professional, or real estate
professional. These calculations are based on my understanding of
the rules as of 2025.

Tax laws are complex and vary by individual circumstances. This
calculator makes simplified assumptions that may not apply to your
specific situation.

Out of scope:
- 1031 exchanges (rental property)
- Step-up basis at death
- Alternative Minimum Tax (AMT)
- State-specific tax credits
- Property depreciation deductions

Please consult a qualified tax professional, financial advisor,
and real estate professional for your specific situation before
making any major financial decisions.
```

## Future Enhancements (Post-MVP)
- Investment property analysis (rental income calculator)
- 1031 exchange scenarios
- Refinance calculator
- Multi-unit property support
- Alternative scenarios comparison (side-by-side 3% vs 20% down)
- Save multiple property comparisons
- Export detailed report to PDF
- Share calculations via URL
- Mobile app version
- Real-time market data integration
