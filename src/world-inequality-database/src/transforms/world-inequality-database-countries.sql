-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Area codes include countries, subnational regions, supranational regions, and synthetic aggregate areas; filter the code or region fields before treating rows as countries.
SELECT
    "alpha2",
    "titlename",
    "shortname",
    "region",
    "region2"
FROM "world-inequality-database-countries"
