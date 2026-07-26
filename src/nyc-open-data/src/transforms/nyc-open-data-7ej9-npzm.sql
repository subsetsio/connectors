-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "location_name",
    "location_category",
    "administrative_district",
    "female_removals",
    "female_principal",
    "female_superintendent",
    "female_expulsions",
    "male_removals",
    "male_principal",
    "male_superintendent",
    "male_expulsions",
    "sy1718_total_removalssuspensions"
FROM "nyc-open-data-7ej9-npzm"
