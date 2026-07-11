-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "king_of_economic_activity",
    CAST("period" AS BIGINT) AS period,
    "value"
FROM "geostat-transport-20and-20communication-investment-20in-20fixed-20assets-investment-in-fixed-assets-by-kind-of-econ-ac"
