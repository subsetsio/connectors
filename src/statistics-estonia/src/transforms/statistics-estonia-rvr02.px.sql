-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "type_of_migration",
    "indicator",
    "sex",
    "administrative_unit_type_of_settlement_region",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rvr02.px"
