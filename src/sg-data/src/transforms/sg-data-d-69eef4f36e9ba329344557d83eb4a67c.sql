-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_inmates",
    "cbp_emplacement_number"
FROM "sg-data-d-69eef4f36e9ba329344557d83eb4a67c"
