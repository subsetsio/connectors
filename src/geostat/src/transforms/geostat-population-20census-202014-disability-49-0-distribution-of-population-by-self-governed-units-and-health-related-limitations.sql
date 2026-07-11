-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disability_categories",
    "health_related_limitations",
    "region_self_governed_unit",
    "value"
FROM "geostat-population-20census-202014-disability-49-0-distribution-of-population-by-self-governed-units-and-health-related-limitations"
