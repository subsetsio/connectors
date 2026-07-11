-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "duration_of_marriage_year",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "geostat-demography-divorces-43-divorces-by-marriage-duration"
