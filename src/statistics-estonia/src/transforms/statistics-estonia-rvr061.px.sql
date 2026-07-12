-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "sex",
    "type_of_settlement_region",
    "age_group",
    "county",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-rvr061.px"
