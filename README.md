# Franchise Cost Dataset (2025 FDDs)

Structured cost data for **623 U.S. franchise brands**, extracted from publicly available Franchise Disclosure Documents (FDDs).

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
  franchise-costs-2025.csv    # 623 brands, 33 columns
  franchise-costs-2025.json   # Same data in JSON format
```

## Categories

623 brands across 22 categories. Labels follow the source FDD taxonomy, so
some food/restaurant buckets overlap (QSR, Restaurant, Restaurants, Food) — a
`groupby("category")` returns exactly these as-filed values. Ranges below are
the per-category **median** investment_low – investment_high.

| Category | Brands | Median Investment |
|----------|--------|-------------------|
| Retail | 207 | $1.5M – $3.5M |
| Restaurants | 101 | $350K – $800K |
| QSR | 57 | $781K – $2.3M |
| Restaurant | 52 | $500K – $1.5M |
| Food | 37 | $469K – $1.1M |
| Home Services | 34 | $128K – $202K |
| Automotive | 24 | $475K – $1.9M |
| Education | 15 | $405K – $600K |
| Fitness | 14 | $470K – $1.1M |
| + 13 more | 82 | varies |

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

> FranchiseVS. (2025). Franchise Cost Dataset: Structured FDD data for 623 U.S. franchise brands. https://franchisevs.com

## Related

- [FranchiseVS](https://franchisevs.com) — interactive franchise cost comparison tool
- [FranchiseVS API](https://franchisevs.com/developers) — REST API for franchise data
- [2025 Franchise Cost Report](https://franchisevs.com/guide/franchise-cost-report-2026) — analysis of investment trends across 170+ brands
