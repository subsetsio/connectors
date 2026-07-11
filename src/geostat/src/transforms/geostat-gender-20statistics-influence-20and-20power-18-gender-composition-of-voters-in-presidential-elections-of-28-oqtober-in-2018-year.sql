-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "voters",
    "gender",
    "region",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-gender-20statistics-influence-20and-20power-18-gender-composition-of-voters-in-presidential-elections-of-28-oqtober-in-2018-year"
