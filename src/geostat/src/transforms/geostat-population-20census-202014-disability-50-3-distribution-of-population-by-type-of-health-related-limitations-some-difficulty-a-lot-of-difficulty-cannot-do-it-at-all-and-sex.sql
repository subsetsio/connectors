-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "type_of_health_related_limitations",
    "value"
FROM "geostat-population-20census-202014-disability-50-3-distribution-of-population-by-type-of-health-related-limitations-some-difficulty-a-lot-of-difficulty-cannot-do-it-at-all-and-sex"
