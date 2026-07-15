-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ethnic_group",
    "gender",
    "death_age",
    "infant_indicator",
    "infant_death_age",
    "death_count"
FROM "sg-data-d-bca761dca17d3155db130b84a8c01a23"
