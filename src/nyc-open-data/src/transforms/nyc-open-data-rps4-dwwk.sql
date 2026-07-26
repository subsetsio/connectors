-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "board",
    "first_name",
    "last_name",
    "year_appointed"
FROM "nyc-open-data-rps4-dwwk"
