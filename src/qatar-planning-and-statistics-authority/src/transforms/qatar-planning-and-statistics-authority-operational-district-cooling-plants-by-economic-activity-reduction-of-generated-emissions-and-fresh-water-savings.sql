-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "economic_activity_ar",
    "economic_activity_category",
    "reduction_in_emissions_compared_to_conventional_cooling_tons_of_co2_equivalent",
    "freshwater_savings_using_treated_wastewater_for_cooling_thousand_m3_year"
FROM "qatar-planning-and-statistics-authority-operational-district-cooling-plants-by-economic-activity-reduction-of-generated-emissions-and-fresh-water-savings"
