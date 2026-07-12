-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    CAST("year" AS BIGINT) AS year,
    "participation_in_adult_education",
    "county",
    "value"
FROM "statistics-estonia-htt351.px"
