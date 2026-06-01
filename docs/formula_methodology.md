# Formula Methodology

## Valuation formula

Estimated value is built from a weighted blend of:

- Comparable-sales value
- Price-per-square-foot value
- Assessed-value signal
- Last-sale-adjusted signal
- Market-trend adjustment
- Optional renovation value add

Default weights:

- Comparable sales: 0.40
- Price per sqft: 0.25
- Assessed value: 0.15
- Last sale adjusted: 0.20

If a source is missing, the system redistributes that weight proportionally across the remaining sources and returns the adjusted weights.

## Comparable adjustment logic

Each comparable is adjusted using:

- Square-footage difference
- Bedroom difference
- Bathroom difference
- Lot-size difference
- Relative age
- Market-time adjustment

The adjusted comparable values are then combined using similarity-aware weighting.

## Renovation formula

General formula:

`Total Cost = Material + Labor + Permit + Disposal + Overhead + Contingency`

Default assumptions:

- Contractor overhead: 15%
- Contingency: 10%
- Labor rate: $65/hour

Specialized scenario logic is included for kitchen, bathroom, and new-build use cases.

## Renovation ROI

`Estimated Value Added = Renovation Cost * Value Multiplier`

Example multipliers:

- Kitchen: 0.70
- Bathroom: 0.65
- Roof: 0.55
- New build: 0.85

## Confidence score

Confidence is scored from 0 to 100 using:

- Data completeness: 40%
- Comparable quality: 35%
- Market data quality: 15%
- Recency: 10%
