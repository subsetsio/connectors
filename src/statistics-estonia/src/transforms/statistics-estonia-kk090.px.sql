-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ecosystem_type",
    "owner_s_economic_activity_and_institutional_sector",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-kk090.px"
