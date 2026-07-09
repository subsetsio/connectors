-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quarterly rows dated to the first month of the quarter. Unlike its sibling chart3 table, `real_gdp` here is the LAGGED (year-ahead) real GDP growth aligned to the quarter in which the `spread` was observed, which is why the most recent quarters have a spread but no GDP value.
-- caution: `recession` is a chart-shading sentinel, not a value: 100 marks a quarter inside an NBER recession and -100 a quarter outside one.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "real_gdp",
    "spread",
    "recession"
FROM "cleveland-fed-yieldcurve-chart4-spread-vs-lagrealgdp"
