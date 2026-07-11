-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    "period",
    "value"
FROM "geostat-business-20statistics-turnover-turnover-by-enterprise-size-and-period-new"
