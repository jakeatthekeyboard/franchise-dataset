# Franchise Cost Dataset (2025 FDDs)

Structured cost data for **172 U.S. franchise brands**, extracted from publicly available Franchise Disclosure Documents (FDDs).

Every franchisor is legally required to file an FDD before selling franchises. These documents contain the real numbers — initial investment ranges, royalty rates, advertising fees, unit counts, financial performance data, and litigation history. This dataset extracts the key data points into a single, comparable format.

## What's in the data

Each row represents one franchise brand with 33 fields:

| Field | Description |
|-------|-------------|
| `brand_name` | Brand name (e.g., McDonald's, Subway) |
| `category` | Industry category (QSR, Home Services, Fitness, etc.) |
| `franchise_fee_low/high` | Initial franchise fee range ($) |
| `investment_low/high` | Total initial investment range from Item 7 ($) |
| `royalty_type` | Percentage, flat fee, or greater-of |
| `royalty_value` | Royalty rate or amount |
| `ad_fund_value` | Advertising/marketing fund contribution |
| `has_item19` | Whether the FDD includes financial performance data |
| `average_gross_revenue` | Average unit revenue (if disclosed) |
| `median_gross_revenue` | Median unit revenue (if disclosed) |
| `total_units` | Total franchise + company-owned locations |
| `net_growth_rate_pct` | Year-over-year unit growth |
| `health_score` | Composite score (0–100) based on growth, fees, and risk |
| `fee_burden_pct` | Total ongoing fees as % of revenue |
| `payback_period_years` | Estimated investment payback period |
| `litigation_total_cases` | Number of legal cases in FDD |
| `litigation_risk_level` | Risk classification |

Full field list in the CSV header.

## Files

```
data/
  franchise-costs-2025.csv    # 172 brands, 33 columns
  franchise-costs-2025.json   # Same data in JSON format
```

## Categories

| Category | Brands | Avg. Investment Range |
|----------|--------|----------------------|
| QSR | 32 | $500K – $2.5M |
| Home Services | 31 | $80K – $250K |
| Food | 17 | $300K – $1.5M |
| Fitness | 14 | $150K – $500K |
| Automotive | 14 | $200K – $600K |
| Education | 12 | $80K – $300K |
| Personal Services | 12 | $100K – $350K |
| Pet | 8 | $150K – $500K |
| Senior Care | 3 | $80K – $200K |
| + 7 more | 29 | varies |

## Quick start

**Python:**
```python
import pandas as pd

df = pd.read_csv("data/franchise-costs-2025.csv")

# Cheapest franchises to open
df.nsmallest(10, "investment_low")[["brand_name", "category", "investment_low", "investment_high"]]

# Average royalty by category
df.groupby("category")["royalty_value"].mean().sort_values()

# Brands with Item 19 financial data
df[df["has_item19"] == "yes"][["brand_name", "median_gross_revenue", "health_score"]]
```

**R:**
```r
df <- read.csv("data/franchise-costs-2025.csv")
head(df[order(df$investment_low), c("brand_name", "category", "investment_low")], 10)
```

## Source & methodology

All data extracted from 2025 FDD filings sourced from state regulatory databases (primarily Minnesota Department of Commerce CARDS system). Extraction was done programmatically with manual verification of key fields.

For an interactive version with filtering, comparison tools, and full brand detail pages, see [franchisevs.com](https://franchisevs.com).

The FranchiseVS API also provides this data programmatically:

```
curl https://franchisevs.com/api/brands
curl https://franchisevs.com/api/brands/mcdonalds
```

## License

This dataset is released under the [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. You're free to use, share, and adapt it for any purpose — just give attribution.

**Suggested citation:**

> FranchiseVS. (2025). Franchise Cost Dataset: Structured FDD data for 172 U.S. franchise brands. https://franchisevs.com

## Related

- [FranchiseVS](https://franchisevs.com) — interactive franchise cost comparison tool
- [FranchiseVS API](https://franchisevs.com/developers) — REST API for franchise data
- [2025 Franchise Cost Report](https://franchisevs.com/guide/franchise-cost-report-2026) — analysis of investment trends across 170+ brands
