-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "commuting_mode",
    "msa",
    "msa_size",
    CAST("percent_of_commuters" AS DOUBLE) AS percent_of_commuters
FROM "u-s-department-of-transportation-ex2n-fgi7"
