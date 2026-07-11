-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "number_of_health_related_limitations",
    "sex",
    "age",
    "value"
FROM "geostat-population-20census-202014-disability-50-17-distribution-of-population-with-health-related-limitations-a-lot-of-difficulty-cannot-do-it-at-all-by-number-of-limitations-sex-and-age"
