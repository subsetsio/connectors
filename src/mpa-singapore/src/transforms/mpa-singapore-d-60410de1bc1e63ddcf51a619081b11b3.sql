-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "purpose_type",
    "number_of_vessel_calls",
    "gross_tonnage"
FROM "mpa-singapore-d-60410de1bc1e63ddcf51a619081b11b3"
