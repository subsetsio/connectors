-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "major_industry",
    "detailed_industry",
    "distribution_by_industry"
FROM "sg-data-d-cc2e7b807ddcdbc14b84188c5f749816"
