-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disability_categories",
    "health_related_limitations",
    "sex",
    "age",
    "value"
FROM "geostat-population-20census-202014-disability-50-distribution-of-population-by-age-health-related-limitations-and-sex"
