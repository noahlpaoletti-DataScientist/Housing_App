# Valuation Model Notes

The current MVP uses formula-driven valuation for transparency and auditability. The repository includes ML scaffolding so a later phase can compare formula outputs against trained baseline models.

Recommended next modeling steps:

- Collect a broader comparable-sales dataset
- Train a baseline regression model
- Compare model residuals to formula outputs
- Build a calibration layer by market/ZIP/property type
- Store model predictions alongside formula estimates for explainability
