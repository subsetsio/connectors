-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disability_categories",
    "health_related_limitations",
    "urban_rural",
    "regions",
    "value"
FROM "geostat-population-20census-202014-disability-49-distribution-of-population-by-regions-and-health-related-limitations"
