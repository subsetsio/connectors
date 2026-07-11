-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    "period",
    "value"
FROM "geostat-construction-construction-20by-20kind-20of-20economic-20activity-20nace-20rev-2-average-20monthly-20earnings-20of-20emploed-20persons-average-monthly-earnings-of-employed-persons-by-size-of-enterprises-new"
