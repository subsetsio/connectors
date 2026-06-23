import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.fca as f

# monkeypatch save_raw_ndjson to capture instead of write
captured={}
def fake_save(rows, asset, **kw): captured[asset]=rows; return "ok"
f.save_raw_ndjson=fake_save

tests=[
 ("fca-firm-complaints", f.fetch_firm_complaints),
 ("fca-product-sales", f.fetch_product_sales),
 ("fca-general-insurance-value-measures", f.fetch_general_insurance_value_measures),
 ("fca-mortgage-lending-statistics", f.fetch_mortgage_lending_statistics),
 ("fca-retail-intermediary-market", f.fetch_retail_intermediary_market),
 ("fca-retirement-income-market", f.fetch_retirement_income_market),
]
import json
for aid, fn in tests:
    try:
        fn(aid)
        rows=captured[aid]
        print(f"\n### {aid}: {len(rows)} rows")
        for r in rows[:2]: print("  ", json.dumps(r, default=str)[:200])
        for r in rows[-1:]: print("  ", json.dumps(r, default=str)[:200])
    except Exception as e:
        import traceback; print(f"\n### {aid}: ERROR {type(e).__name__}: {e}"); traceback.print_exc()
