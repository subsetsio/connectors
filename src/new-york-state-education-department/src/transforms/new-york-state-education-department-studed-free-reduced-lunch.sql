-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Free and reduced-price lunch counts are related poverty-proxy measures on the same institution-year row.
SELECT
    "report_year",
    "entity_cd",
    "entity_name",
    "year",
    "num_free_lunch",
    "per_free_lunch",
    "num_reduced_lunch",
    "per_reduced_lunch"
FROM "new-york-state-education-department-studed-free-reduced-lunch"
