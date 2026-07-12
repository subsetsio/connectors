-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "sector_of_economy",
    "group_of_persons",
    "sex",
    "indicator",
    "value"
FROM "statistics-estonia-tt207.px"
