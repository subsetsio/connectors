-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ownership_types",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-business-20statistics-intermediate-20consumption-intermediate-consumption-owner"
