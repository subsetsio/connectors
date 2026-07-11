-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "types_of_economic_activities",
    "production",
    "value"
FROM "geostat-national-20accounts-system-20of-20national-20accounts-201993-20-28sna-201993-29-supply-use-20tables-2016-supply-2016-15-15-en"
