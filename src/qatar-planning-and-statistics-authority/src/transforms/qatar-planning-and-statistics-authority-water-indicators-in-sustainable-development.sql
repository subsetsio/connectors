-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "goal",
    "target",
    "indicator",
    "indicator_name",
    "proportion_value",
    "proportion_percentage",
    "value_added_of_agricultural_activities_at_constant_prices_2018_qr_amount_of_water_used_in_the_agricu",
    "value_added_of_industrial_activities_at_constant_prices_2018_qr_amount_of_water_used_in_the_industri",
    "value_added_of_commercial_activities_at_constant_prices_2018_qr_amount_of_water_used_in_the_commerci"
FROM "qatar-planning-and-statistics-authority-water-indicators-in-sustainable-development"
