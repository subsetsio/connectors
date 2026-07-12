-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "language_region",
    "cancer_site",
    "sex",
    "period",
    "age_class",
    "indicator",
    "measure",
    "value",
    "cube_id",
    "updated"
FROM "federal-statistical-office-px-x-1403030300-161"
