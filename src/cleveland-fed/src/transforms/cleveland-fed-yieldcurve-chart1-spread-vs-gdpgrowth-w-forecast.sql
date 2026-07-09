-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quarterly rows dated to the first month of the quarter. The table mixes realized history with a model forecast extending years into the future: on forecast rows only `real_gdp_growth_forecast` is populated, on historical rows only `real_gdp_growth`. Never treat the two as one column without deciding which regime you want.
-- caution: The file also carries a quarter-average-spread annotation column whose NAME encodes the averaging window (e.g. `spread_qtavg_04012026_06192026`) and therefore changes every quarter.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "spread",
    "real_gdp_growth",
    "real_gdp_growth_forecast",
    "spread_qtavg_04012026_06192026"
FROM "cleveland-fed-yieldcurve-chart1-spread-vs-gdpgrowth-w-forecast"
