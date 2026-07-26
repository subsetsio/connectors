-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "report_date",
    "borough",
    "community_district",
    "case_type",
    "cases",
    "individuals"
FROM "nyc-open-data-ur7y-ziyb"
