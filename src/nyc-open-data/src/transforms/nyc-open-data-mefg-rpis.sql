-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_no",
    "report_date",
    "indicator_name",
    "indicator_value"
FROM "nyc-open-data-mefg-rpis"
