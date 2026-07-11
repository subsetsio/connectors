-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "region_self_governed_unit",
    "value"
FROM "geostat-demography-divorces-41-divorces-by-regions-and-self-governed-units"
