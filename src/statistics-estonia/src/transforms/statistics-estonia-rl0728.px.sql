-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_institution",
    "age_group",
    "sex",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0728.px"
