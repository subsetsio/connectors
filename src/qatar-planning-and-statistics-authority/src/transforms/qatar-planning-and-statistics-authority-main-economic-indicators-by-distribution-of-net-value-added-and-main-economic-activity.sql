-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "activity_code",
    "main_economic_activity",
    "main_economic_activity_ar",
    "distribution_of_net_value_added_value_qr_000_operatin",
    "distribution_of_net_value_added_value_qr_000_compens"
FROM "qatar-planning-and-statistics-authority-main-economic-indicators-by-distribution-of-net-value-added-and-main-economic-activity"
