-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "epi_year",
    "epi_week",
    "est_count"
FROM "sg-data-d-11e68bba3b3c76733475a72d09759eeb"
