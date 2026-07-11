-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include separate Global, Northern Hemisphere, and Southern Hemisphere series; filter `region` before interpreting a single regional trend.
SELECT
    "date",
    "region",
    "anomaly_c",
    "lower_95_c",
    "upper_95_c"
FROM "met-office-hadcrut5-hadcrut5-monthly"
