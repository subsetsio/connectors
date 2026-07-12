-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "age_group_of_bride",
    "age_group_of_groom",
    "place_of_residence_of_groom",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv286u.px"
