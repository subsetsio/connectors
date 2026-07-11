-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "enterprise_size",
    "period",
    "value"
FROM "geostat-transport-20and-20communication-average-20monthly-20remuneration-20of-20employed-20persons-average-monthly-remuneration-by-ec-ac"
