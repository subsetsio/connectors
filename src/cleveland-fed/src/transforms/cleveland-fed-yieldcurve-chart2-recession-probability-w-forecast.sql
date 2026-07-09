-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Monthly rows dated to the first of the month, extending years into the future: `recession_probability` is the estimated probability (percent) over realized history and `recession_probability_forecast` over the forecast horizon; exactly one of the two is populated on any row.
-- caution: `recession` is a chart-shading sentinel, not a value: 1000 marks a month inside an NBER recession and 0 a month outside one.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "recession_probability",
    "recession_probability_forecast",
    "recession"
FROM "cleveland-fed-yieldcurve-chart2-recession-probability-w-forecast"
