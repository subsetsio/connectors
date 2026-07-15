-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "ethnic_group",
    "crude_death_rate",
    "crude_birth_rate",
    "crude_natural_inc_rate"
FROM "sg-data-d-b1516a82d21dc594ad5a93cc341a234c"
