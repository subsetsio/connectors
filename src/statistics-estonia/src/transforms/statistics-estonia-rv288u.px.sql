-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month_of_divorce",
    "place_of_residence_of_groom_or_older_spouse",
    "type_of_settlement_region",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rv288u.px"
