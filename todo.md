# Rent vs. Buy Calculator - Todo List

## Milestone 1: UI Setup with Dummy Data ✅

### Project Setup
- [ ] Initialize React + Vite project with `npm create vite@latest`
- [ ] Install dependencies:
  - [ ] Tailwind CSS
  - [ ] PostCSS and Autoprefixer
  - [ ] React Icons (for visual indicators)
- [ ] Configure Tailwind CSS
- [ ] Set up basic project structure (folders for components, utils, hooks)
- [ ] Clean up default Vite boilerplate

### Constants and Presets
- [ ] Create `src/utils/constants.js` file
  - [ ] Add LOCATION_PRESETS (SF, Redwood City, Palo Alto)
  - [ ] Add DEFAULT_ASSUMPTIONS (tax rates, insurance, maintenance, etc.)
  - [ ] Add STANDARD_DEDUCTION constants
  - [ ] Add CAPITAL_GAINS_EXCLUSION constants

### Component Development

#### Input Components
- [ ] Create `src/components/LocationPresets.jsx`
  - [ ] Button group for SF / Redwood City / Palo Alto / Custom
  - [ ] Auto-populate purchase price and monthly rent on selection

- [ ] Create `src/components/InputForm.jsx`
  - [ ] **Property Information**
    - [ ] Purchase Price input (currency)
    - [ ] Monthly Rent input (currency)
  - [ ] **Financing Options**
    - [ ] Down Payment Percentage (3%, 20%, 100% radio buttons or dropdown)
    - [ ] Interest Rate (5% or 6% radio buttons)
    - [ ] Loan Term (fixed at 30 years, display only)
  - [ ] "Calculate" button
  - [ ] "Clear" button

- [ ] Create `src/components/TaxInputs.jsx`
  - [ ] Filing Status (Single / Married radio buttons)
  - [ ] W-2 Income input (currency)
  - [ ] Federal Tax Bracket input (percentage)
  - [ ] State Tax Rate input (percentage)
  - [ ] State Income Tax Paid input (currency, for SALT)

- [ ] Create `src/components/AssumptionsPanel.jsx`
  - [ ] Collapsible "Advanced Assumptions" section
  - [ ] Property Tax Rate (default 1.2%)
  - [ ] Homeowners Insurance (default $3,000)
  - [ ] Renters Insurance (default $200)
  - [ ] PMI Rate (default 1%)
  - [ ] Buying Closing Costs (default $30,000)
  - [ ] Selling Closing Costs (default $30,000)
  - [ ] Selling Commission (default 6%)
  - [ ] Appreciation Rate (3% or 7% toggle)
  - [ ] Rent Inflation Rate (default 3%)
  - [ ] Maintenance costs (roof, water heater, flooring)
  - [ ] "Reset to Defaults" button

#### Results Components
- [ ] Create `src/components/ResultsSummary.jsx`
  - [ ] Display "Total Cost of Renting (30 years)" with dummy data
  - [ ] Display "Total Cost of Buying (30 years)" with dummy data
  - [ ] Display winner (Renting or Buying) with color coding
  - [ ] Display "Break-even Year" with dummy data
  - [ ] Display "Total Tax Savings from Homeownership" with dummy data

- [ ] Create `src/components/TaxBenefitsCard.jsx`
  - [ ] Display "Year 1 Tax Benefit Analysis" section
  - [ ] Show Mortgage Interest Paid (with cap notation)
  - [ ] Show Property Taxes Paid
  - [ ] Show State Income Tax Paid
  - [ ] Show SALT Deduction (with $10K cap notation)
  - [ ] Show Total Itemized Deductions
  - [ ] Show Standard Deduction (for comparison)
  - [ ] Show Excess Deductions
  - [ ] Show Net Tax Savings (highlighted in green)
  - [ ] All with dummy data

- [ ] Create `src/components/CapitalGainsCard.jsx`
  - [ ] Display "Sale Proceeds Analysis (Year 30)" section
  - [ ] Show Sale Price (with appreciation)
  - [ ] Show Total Capital Gain
  - [ ] Show Capital Gains Exclusion amount
  - [ ] Show Taxable Gain (if any)
  - [ ] Show Capital Gains Tax Owed
  - [ ] Show Net Proceeds to Seller
  - [ ] All with dummy data

- [ ] Create `src/components/AnnualTable.jsx`
  - [ ] Table with columns:
    - [ ] Year
    - [ ] Rent Paid
    - [ ] Mortgage Payment
    - [ ] Property Tax
    - [ ] Insurance
    - [ ] Maintenance
    - [ ] PMI
    - [ ] Tax Benefit
    - [ ] Property Value
    - [ ] Home Equity
    - [ ] Cumulative Cost (Rent)
    - [ ] Cumulative Cost (Buy)
  - [ ] Display first 5 years with dummy data
  - [ ] "Show All 30 Years" expand button

- [ ] Create `src/components/MetricCard.jsx`
  - [ ] Reusable card component for displaying metrics
  - [ ] Props: title, value, icon, color, tooltip, subtitle
  - [ ] Responsive styling

### Layout and Styling
- [ ] Create main `App.jsx` layout
  - [ ] Header with app title: "Rent vs. Buy Calculator with Tax Benefits"
  - [ ] Disclaimer section (educational purposes, not financial advice)
  - [ ] Location presets at top
  - [ ] Two-column layout:
    - [ ] Left: Input forms (Property, Financing, Tax, Assumptions)
    - [ ] Right: Results (Summary, Tax Benefits, Capital Gains, Annual Table)
  - [ ] Footer with attribution and disclaimer

- [ ] Implement responsive design
  - [ ] Desktop layout (side-by-side)
  - [ ] Tablet layout (stacked with padding)
  - [ ] Mobile layout (single column, inputs first, then results)

- [ ] Apply Tailwind CSS styling
  - [ ] Color scheme (blue primary, green success, red danger)
  - [ ] Typography styles
  - [ ] Form input styles (labels, borders, focus states)
  - [ ] Button styles (primary, secondary, clear)
  - [ ] Card styles for results
  - [ ] Table styles (striped rows, responsive)

### Dummy Data Setup
- [ ] Create dummy calculation results object in App.jsx:
  ```javascript
  const DUMMY_RESULTS = {
    totalCostRenting30: 3500000,
    totalCostBuying30: 3200000,
    breakEvenYear: 12,
    totalTaxSavings: 180000,
    year1TaxBenefit: {
      mortgageInterest: 45000,
      propertyTax: 24000,
      stateIncomeTax: 30000,
      saltDeduction: 10000,
      totalItemized: 55000,
      standardDeduction: 31500,
      excessDeductions: 23500,
      taxSavings: 9706
    },
    capitalGains: {
      purchasePrice: 2000000,
      salePrice: 4000000,
      capitalGain: 2000000,
      exclusion: 500000,
      taxableGain: 1500000,
      capitalGainsTax: 300000,
      netProceeds: 2100000
    },
    annualData: [
      // First 5 years with dummy data
    ]
  }
  ```

### Testing and Polish
- [ ] Test app runs on localhost (`npm run dev`)
- [ ] Verify all input fields render correctly
- [ ] Verify location presets populate prices correctly
- [ ] Verify all results sections display with dummy data
- [ ] Test responsive layout on different screen sizes
- [ ] Check for console errors
- [ ] Verify disclaimer is prominently displayed
- [ ] Test in different browsers (Chrome, Firefox, Safari)

### Documentation
- [ ] Add comments to code where needed
- [ ] Create basic README.md with setup instructions

---

## Milestone 2: Implement Real Calculations 🔜

### Calculation Utilities

#### Mortgage Calculations
- [ ] Create `src/utils/mortgageCalculations.js`
- [ ] Implement `calculateMonthlyPayment(principal, annualRate, years)`
  - [ ] Use formula: M = P * [r(1+r)^n] / [(1+r)^n-1]
  - [ ] Return monthly P&I payment
  - [ ] Handle edge case: 100% down payment (no mortgage)

- [ ] Implement `generateAmortizationSchedule(principal, annualRate, years)`
  - [ ] Return array of 360 monthly payments
  - [ ] Each entry: { month, payment, principal, interest, remainingBalance }
  - [ ] Used for calculating annual interest paid

- [ ] Implement `calculateAnnualInterestPaid(amortization, year)`
  - [ ] Sum interest from months (year-1)*12+1 to year*12
  - [ ] Return annual interest amount

- [ ] Implement `calculatePMI(purchasePrice, downPaymentPercent)`
  - [ ] If downPaymentPercent < 20, return purchasePrice * 1%
  - [ ] Else return 0

- [ ] Implement `calculatePMIStopYear(purchasePrice, downPaymentPercent, amortization, appreciationRate)`
  - [ ] PMI stops when equity reaches 20% of original purchase price
  - [ ] Equity = (currentValue - remainingBalance)
  - [ ] Return year when PMI stops

#### Tax Calculations
- [ ] Create `src/utils/taxCalculations.js`
- [ ] Implement `calculateDeductibleMortgageInterest(totalInterest, mortgageBalance)`
  - [ ] Cap at interest on $750K of debt
  - [ ] If mortgageBalance > 750000, prorate
  - [ ] Return deductible interest amount

- [ ] Implement `calculateSALTDeduction(propertyTax, stateIncomeTax)`
  - [ ] Sum property tax + state income tax
  - [ ] Cap at $10,000
  - [ ] Return SALT deduction amount

- [ ] Implement `calculateItemizedDeductions(deductibleInterest, saltDeduction)`
  - [ ] Sum deductible mortgage interest + SALT
  - [ ] Return total itemized deductions

- [ ] Implement `calculateTaxSavings(itemizedDeductions, filingStatus, federalRate, stateRate)`
  - [ ] Get standard deduction based on filing status
  - [ ] Calculate excess: MAX(0, itemized - standard)
  - [ ] Calculate combined tax rate: federal + state
  - [ ] Return excess * combinedRate

- [ ] Implement `calculateAnnualTaxBenefit(year, amortization, inputs)`
  - [ ] Calculate for specific year
  - [ ] Return object with all tax benefit details
  - [ ] Handle decreasing interest over time

- [ ] Implement `calculateCapitalGains(purchasePrice, appreciationRate, years, filingStatus)`
  - [ ] Calculate sale price: purchasePrice * (1 + rate)^years
  - [ ] Calculate capital gain: salePrice - purchasePrice
  - [ ] Get exclusion based on filing status
  - [ ] Calculate taxable gain: MAX(0, gain - exclusion)
  - [ ] Calculate tax: taxableGain * 20%
  - [ ] Return detailed breakdown

#### Rent vs Buy Calculations
- [ ] Create `src/utils/rentVsBuyCalculations.js`
- [ ] Implement `calculateTotalCostOfRenting(monthlyRent, inflationRate, years, rentersInsurance)`
  - [ ] Loop through each year
  - [ ] Year 1: monthlyRent * 12
  - [ ] Year N: prevYearRent * (1 + inflationRate)
  - [ ] Add renters insurance (with inflation)
  - [ ] Return total cumulative cost

- [ ] Implement `calculateYearlyOwnershipCosts(year, inputs, amortization)`
  - [ ] Mortgage payment (from amortization)
  - [ ] Property tax (with 2% annual increase)
  - [ ] Homeowners insurance (with 3% inflation)
  - [ ] PMI (if applicable, until equity reaches 20%)
  - [ ] Maintenance costs (roof, water heater, flooring amortized, with inflation)
  - [ ] Return total cost for that year

- [ ] Implement `calculateNetProceedsFromSale(inputs, amortization, years)`
  - [ ] Sale price (with appreciation)
  - [ ] Minus: remaining mortgage balance
  - [ ] Minus: selling closing costs ($30K)
  - [ ] Minus: selling commission (6% of sale price)
  - [ ] Minus: capital gains tax (from calculateCapitalGains)
  - [ ] Return net proceeds

- [ ] Implement `calculateTotalCostOfBuying(inputs)`
  - [ ] Down payment
  - [ ] Buying closing costs ($30K)
  - [ ] Sum of all mortgage payments (30 years)
  - [ ] Sum of all property taxes (with 2% increases)
  - [ ] Sum of all insurance (with 3% inflation)
  - [ ] Sum of all maintenance (with 3% inflation)
  - [ ] Sum of all PMI (until stop year)
  - [ ] Minus: Total tax savings (sum of 30 years)
  - [ ] Minus: Net proceeds from sale
  - [ ] Return total cost

- [ ] Implement `calculateBreakEvenYear(inputs)`
  - [ ] Loop through years 1-30
  - [ ] Calculate cumulative cost of renting
  - [ ] Calculate cumulative cost of buying
  - [ ] Return first year where buying < renting
  - [ ] If never breaks even, return null

- [ ] Implement `generateAnnualBreakdown(inputs)`
  - [ ] Loop through years 1-30
  - [ ] For each year, calculate:
    - [ ] Rent paid (with inflation)
    - [ ] Mortgage payment
    - [ ] Property tax
    - [ ] Insurance
    - [ ] Maintenance
    - [ ] PMI
    - [ ] Tax benefit
    - [ ] Property value
    - [ ] Remaining balance
    - [ ] Home equity
    - [ ] Cumulative cost rent
    - [ ] Cumulative cost buy
  - [ ] Return array of 30 year objects

#### Formatters
- [ ] Create `src/utils/formatters.js`
- [ ] Implement `formatCurrency(value)`
  - [ ] Format as $1,234,567 (with commas, no decimals for large numbers)
  - [ ] Format as $1,234.56 (with decimals for small numbers)

- [ ] Implement `formatPercentage(value, decimals = 1)`
  - [ ] Format as 12.5%

- [ ] Implement `formatNumber(value)`
  - [ ] Add thousand separators

#### Validation
- [ ] Create `src/utils/validation.js`
- [ ] Implement validation functions:
  - [ ] `validatePositiveNumber(value)`
  - [ ] `validatePercentage(value)` (0-100)
  - [ ] `validateRequired(value)`
  - [ ] `validatePurchasePrice(value)` (min $100K)
  - [ ] `validateRent(value)` (min $500)

### State Management
- [ ] Create `src/hooks/useRentVsBuy.js`
- [ ] Set up state for all inputs:
  - [ ] Property info (price, rent, location)
  - [ ] Financing (downPayment%, interestRate)
  - [ ] Tax info (filing, income, brackets, state tax)
  - [ ] Assumptions (all defaults)
- [ ] Create `calculateAll()` function that:
  - [ ] Runs all calculation utilities
  - [ ] Returns complete results object
  - [ ] Handles errors gracefully
- [ ] Add debouncing (300ms) for performance
- [ ] Export state and handlers

### Integration
- [ ] Connect input forms to state management
- [ ] Connect location presets to auto-populate
- [ ] Wire up Calculate button to trigger calculations
- [ ] Update all results components with real data
- [ ] Remove dummy data
- [ ] Handle loading states during calculations
- [ ] Show error messages for invalid inputs

### Testing
- [ ] Test with provided example scenario:
  - [ ] Married, $400K income, $2M home, 20% down, 6%
  - [ ] Verify Year 1 tax savings = ~$9,706
  - [ ] Verify deductible interest = ~$45,000
  - [ ] Verify SALT deduction = $10,000
  - [ ] Verify total itemized = $55,000

- [ ] Test edge cases:
  - [ ] 3% down payment (with PMI)
  - [ ] 100% down payment (no mortgage, no interest deduction)
  - [ ] Single vs Married filing
  - [ ] High appreciation (7%) vs low (3%)
  - [ ] Different locations (SF, Palo Alto, etc.)

- [ ] Test year-by-year breakdown accuracy
- [ ] Verify break-even calculation
- [ ] Verify capital gains exclusion works correctly

---

## Milestone 3: Enhanced Features & Polish 🔮

### Data Visualization
- [ ] Install Chart.js or Recharts
- [ ] Create `src/components/BreakEvenChart.jsx`
  - [ ] Line chart showing cumulative cost over 30 years
  - [ ] Two lines: Renting vs Buying
  - [ ] Mark break-even point
  - [ ] Make responsive

- [ ] Create expense breakdown pie chart
  - [ ] Show mortgage vs tax vs insurance vs maintenance

### Save and Load
- [ ] Implement save to localStorage
  - [ ] Save button
  - [ ] Auto-generate calculation name/date
- [ ] Create calculation history viewer
  - [ ] List saved calculations
  - [ ] Load calculation button
  - [ ] Delete calculation button
- [ ] Add "Clear All" button with confirmation

### Comparison Tool
- [ ] Create scenario comparison feature
  - [ ] Compare 3% vs 20% down side-by-side
  - [ ] Compare 5% vs 6% interest side-by-side
  - [ ] Compare 3% vs 7% appreciation side-by-side

### Export and Sharing
- [ ] Add export to CSV functionality
  - [ ] Export annual breakdown table
  - [ ] Export summary results
- [ ] Add print-friendly stylesheet
  - [ ] Print button
  - [ ] Hide unnecessary UI elements when printing
  - [ ] Format tables for printing

### User Experience Enhancements
- [ ] Add tooltips to all inputs explaining what they mean
- [ ] Add info icons with explanations:
  - [ ] What is SALT deduction?
  - [ ] What is mortgage interest cap?
  - [ ] What is PMI?
  - [ ] What is capital gains exclusion?
- [ ] Add help modal with FAQs
- [ ] Add smooth scroll to results after calculation
- [ ] Add loading spinner during calculations
- [ ] Add success animation when calculation completes

### Advanced Features
- [ ] Add time horizon selector (5, 10, 15, 20, 25, 30 years)
- [ ] Add "What-if" scenarios:
  - [ ] What if I rent and invest the down payment?
  - [ ] What if property appreciates less/more?
- [ ] Add amortization schedule viewer (Milestone 1 feature)
  - [ ] Show full 30-year schedule
  - [ ] Filterable/sortable

### Polish and Optimization
- [ ] Performance optimization
  - [ ] Memoize expensive calculations
  - [ ] Use React.memo for components
  - [ ] Lazy load charts
- [ ] Add dark mode toggle (optional)
- [ ] Smooth animations and transitions
- [ ] Loading skeletons for results
- [ ] Error boundaries for error handling
- [ ] Accessibility improvements:
  - [ ] ARIA labels
  - [ ] Keyboard navigation
  - [ ] Screen reader testing

### Testing and Quality
- [ ] Cross-browser testing (Chrome, Firefox, Safari, Edge)
- [ ] Mobile device testing (iPhone, Android)
- [ ] Tablet testing (iPad)
- [ ] Accessibility audit (Lighthouse, axe)
- [ ] Performance audit (Lighthouse)
- [ ] Fix all console warnings
- [ ] Code review and refactoring
- [ ] Add PropTypes or TypeScript types

### Documentation
- [ ] Write comprehensive README
  - [ ] What the calculator does
  - [ ] How to use it
  - [ ] Tech stack
  - [ ] Setup instructions
  - [ ] Calculation methodology
- [ ] Add inline code documentation
- [ ] Document all calculation formulas
- [ ] Add screenshots to README
- [ ] Create user guide section

---

## Git/GitHub Tasks

### Version Control
- [ ] Initialize git repository
- [ ] Create .gitignore file
- [ ] Make initial commit with spec, todo, .claude.md
- [ ] Create GitHub repository
- [ ] Push to GitHub
- [ ] Commit after Milestone 1 complete
- [ ] Commit after Milestone 2 complete
- [ ] Commit after Milestone 3 complete

---

## Validation Checklist

### Calculation Accuracy
- [ ] Mortgage payment matches online calculators
- [ ] Amortization schedule is correct
- [ ] Tax benefit calculation matches example ($9,706)
- [ ] SALT cap ($10K) is enforced
- [ ] Mortgage interest cap ($750K) is enforced
- [ ] PMI stops at correct time (20% equity)
- [ ] Capital gains exclusion works correctly
- [ ] Property appreciation compounds correctly
- [ ] Inflation applies to all expenses correctly

### User Experience
- [ ] All inputs have clear labels
- [ ] Error messages are helpful
- [ ] Results update in real-time (debounced)
- [ ] Mobile experience is smooth
- [ ] Disclaimer is prominent and clear
- [ ] Loading states provide feedback

---

## Notes
- Follow tutorial methodology: Plan → Spec → Todo → Code
- Use plan mode before coding new features
- Test frequently on localhost
- Commit to GitHub after each milestone
- Keep it simple - avoid over-engineering
- Focus on accuracy of calculations above all else
- The tax benefit calculation is the most complex part - test thoroughly
