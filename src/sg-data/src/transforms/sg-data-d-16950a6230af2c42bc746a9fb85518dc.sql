-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ethnic_group",
    "live_births",
    "deaths",
    "natural_increase"
FROM "sg-data-d-16950a6230af2c42bc746a9fb85518dc"
