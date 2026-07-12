-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_minor_children",
    CAST("year" AS BIGINT) AS year,
    "household_structure",
    "type_and_tenure_status_of_dwelling",
    "place_of_residence",
    "value"
FROM "statistics-estonia-rlv821.px"
