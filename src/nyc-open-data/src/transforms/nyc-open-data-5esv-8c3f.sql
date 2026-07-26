-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("year_month", '%Y-%m')::DATE AS year_month,
    "industry",
    "total_crashes",
    "total_crashed_vehicles",
    "crashed_vehicles_any_injury",
    "crashed_vehicles_critical_injury",
    "crashed_vehicles_fatality"
FROM "nyc-open-data-5esv-8c3f"
