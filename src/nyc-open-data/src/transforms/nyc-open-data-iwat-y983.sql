-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date_range_of_data",
    "facility",
    "report_category",
    "total",
    "age_7",
    "age_712",
    "age_1317",
    "age_1820",
    "_unknown" AS unknown
FROM "nyc-open-data-iwat-y983"
