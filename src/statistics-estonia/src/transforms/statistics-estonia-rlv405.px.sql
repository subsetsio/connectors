-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "educational_attainment",
    CAST("year" AS BIGINT) AS year,
    "sex",
    "age_group",
    "legal_amrital_status",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv405.px"
