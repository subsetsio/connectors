-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "purpose_of_using_social_media",
    "number_of_persons_employed",
    "economic_activity_emtak_2008",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-it142.px"
