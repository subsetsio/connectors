-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("refernce_period" AS BIGINT) AS refernce_period,
    "indicator",
    "age",
    "sex",
    "county",
    "value"
FROM "statistics-estonia-ht043.px"
