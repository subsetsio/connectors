-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "location_of_educational_institution",
    "mother_tongue",
    "acquired_educational_attainment",
    "age_group",
    "county",
    "sex",
    "value"
FROM "statistics-estonia-rl0314.px"
