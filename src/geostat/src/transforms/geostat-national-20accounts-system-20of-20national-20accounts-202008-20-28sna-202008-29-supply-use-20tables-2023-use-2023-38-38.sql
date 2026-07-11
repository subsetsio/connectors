-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "types_of_economic_activities",
    "products",
    "value"
FROM "geostat-national-20accounts-system-20of-20national-20accounts-202008-20-28sna-202008-29-supply-use-20tables-2023-use-2023-38-38"
