-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Every row is a FORECAST: quarterly projected federal funds rates, in percent per year, for quarters that have not happened yet. There is no realized history in this table.
-- caution: The columns are order statistics ACROSS seven simple monetary policy rules evaluated for that quarter, not five distinct rates: `maximum` and `minimum` are the envelope of the seven rule prescriptions. Each column traces different rules in different quarters, so a column is not a time series of one rule.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "maximum",
    "75th_percentile",
    "median",
    "25th_percentile",
    "minimum"
FROM "cleveland-fed-policyrules-chartdata"
