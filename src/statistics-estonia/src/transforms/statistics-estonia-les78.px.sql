-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "distance_from_the_place_of_residence_of_the_most_frequent_contact_person",
    "age_group",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-les78.px"
