-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "frequency_of_interaction_with_main_contact_person",
    "age_group",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-les80.px"
