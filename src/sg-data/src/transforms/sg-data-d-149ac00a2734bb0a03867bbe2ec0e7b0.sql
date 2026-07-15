-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "qtr",
    "project_name",
    "postal_district",
    "25th_percentile",
    "median",
    "75th_percentile",
    "rental_contracts"
FROM "sg-data-d-149ac00a2734bb0a03867bbe2ec0e7b0"
