-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "locationcode",
    "location_name",
    "location_category_description",
    "gender_sexuality_alliance",
    "lgbtqgnc_training_teachers",
    "lgbtqgnc_training_admin",
    "lgbtqgnc_training_other"
FROM "nyc-open-data-9tg9-e2ph"
