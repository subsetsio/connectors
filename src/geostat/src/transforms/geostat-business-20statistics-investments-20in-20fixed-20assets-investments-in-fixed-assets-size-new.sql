-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-business-20statistics-investments-20in-20fixed-20assets-investments-in-fixed-assets-size-new"
