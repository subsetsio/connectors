-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quarterly rows dated to the first month of the quarter. `spread` is the 10-year minus 3-month Treasury yield spread in percentage points and `real_gdp` the contemporaneous real GDP growth rate; the earliest quarters have no spread observation.
-- caution: `recession` is a chart-shading sentinel, not a value: 100 marks a quarter inside an NBER recession and -100 a quarter outside one.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "real_gdp",
    "spread",
    "recession"
FROM "cleveland-fed-yieldcurve-chart3-spread-vs-realgdp"
