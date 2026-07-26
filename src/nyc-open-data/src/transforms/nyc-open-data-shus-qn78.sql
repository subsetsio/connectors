-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sample_site",
    "sample_id",
    "analyte",
    "sample_date",
    "qualifier"
FROM "nyc-open-data-shus-qn78"
