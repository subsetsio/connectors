-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "disability_categories",
    "health_related_limitations",
    "disability_status",
    "value"
FROM "geostat-population-20census-202014-disability-49-51-distribution-of-population-by-health-related-limitations-and-disability-status"
