#!/usr/bin/env python3
"""Export FranchiseVS data into public dataset formats (CSV + JSON)."""

import csv
import json
import os
import glob

SRC = "/Users/jake/dev/franchisevs/src/data"
OUT = os.path.dirname(os.path.abspath(__file__))

SKIP = {"categories.json", "state-guides.json", "state-guides-b.json", "franchises.json"}

def safe(val):
    if val is None:
        return ""
    return val

def pct(val):
    if val is None:
        return ""
    if isinstance(val, (int, float)):
        return round(val * 100, 2) if val < 1 else val
    return val

def royalty_str(fees):
    r = fees.get("royalty", {})
    if not r:
        return "", "", ""
    rtype = r.get("type", "")
    rval = r.get("value")
    rbasis = r.get("basis", "")
    return rtype, safe(rval), rbasis

def ad_fund_val(fees):
    af = fees.get("ad_fund", {})
    if not af:
        return ""
    return safe(af.get("value"))

def main():
    brands = []
    files = sorted(glob.glob(os.path.join(SRC, "*.json")))

    for fp in files:
        fname = os.path.basename(fp)
        if fname in SKIP:
            continue

        with open(fp) as f:
            try:
                d = json.load(f)
            except json.JSONDecodeError:
                continue

        if "franchisor" not in d:
            continue

        fr = d["franchisor"]
        inv = d.get("initial_investment", {})
        fees_init = d.get("initial_fees", {})
        fees_ong = d.get("ongoing_fees", {})
        fp_data = d.get("financial_performance", {})
        units = d.get("unit_data", {})
        contract = d.get("contract_terms", {})
        lit = d.get("litigation_summary", {})
        metrics = d.get("derived_metrics", {})
        filing = d.get("latest_filing", {})

        royalty_type, royalty_value, royalty_basis = royalty_str(fees_ong)

        row = {
            "brand_name": fr.get("brand_name", ""),
            "slug": fr.get("slug", ""),
            "category": fr.get("category", ""),
            "subcategory": fr.get("subcategory", ""),
            "year_founded": safe(fr.get("year_founded")),
            "year_franchising_began": safe(fr.get("year_franchising_began")),
            "headquarters_state": safe(fr.get("headquarters_state")),
            "fdd_year": safe(filing.get("fdd_year")),
            "franchise_fee_low": safe(fees_init.get("franchise_fee", {}).get("low")),
            "franchise_fee_high": safe(fees_init.get("franchise_fee", {}).get("high")),
            "investment_low": safe(inv.get("total", {}).get("low")),
            "investment_high": safe(inv.get("total", {}).get("high")),
            "royalty_type": royalty_type,
            "royalty_value": royalty_value,
            "royalty_basis": royalty_basis,
            "ad_fund_value": ad_fund_val(fees_ong),
            "has_item19": "yes" if fp_data.get("has_item19") else "no",
            "average_gross_revenue": safe(fp_data.get("average_gross_revenue")),
            "median_gross_revenue": safe(fp_data.get("median_gross_revenue")),
            "total_units": safe(units.get("total_units")),
            "total_franchised": safe(units.get("total_franchised")),
            "total_company_owned": safe(units.get("total_company_owned")),
            "opened_this_year": safe(units.get("opened_this_year")),
            "closed_this_year": safe(units.get("closed_this_year")),
            "net_change": safe(units.get("net_change")),
            "net_growth_rate_pct": safe(metrics.get("net_growth_rate_pct")),
            "term_length_years": safe(contract.get("term_length_years")),
            "territory_exclusive": safe(contract.get("territory_exclusive")),
            "health_score": safe(metrics.get("health_score")),
            "fee_burden_pct": safe(metrics.get("fee_burden_pct")),
            "payback_period_years": safe(metrics.get("payback_period_years")),
            "litigation_total_cases": safe(lit.get("total_cases")),
            "litigation_risk_level": safe(lit.get("risk_level")),
        }
        brands.append(row)

    brands.sort(key=lambda x: x["brand_name"])

    csv_path = os.path.join(OUT, "data", "franchise-costs-2025.csv")
    json_path = os.path.join(OUT, "data", "franchise-costs-2025.json")
    os.makedirs(os.path.join(OUT, "data"), exist_ok=True)

    fields = list(brands[0].keys())
    with open(csv_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(brands)

    with open(json_path, "w") as f:
        json.dump(brands, f, indent=2)

    print(f"Exported {len(brands)} brands")
    print(f"  CSV: {csv_path}")
    print(f"  JSON: {json_path}")

if __name__ == "__main__":
    main()
