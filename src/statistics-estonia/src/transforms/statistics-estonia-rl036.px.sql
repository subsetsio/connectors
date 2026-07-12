-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "size_of_local_government_unit",
    "age_group",
    "sex",
    "value"
FROM "statistics-estonia-rl036.px"
