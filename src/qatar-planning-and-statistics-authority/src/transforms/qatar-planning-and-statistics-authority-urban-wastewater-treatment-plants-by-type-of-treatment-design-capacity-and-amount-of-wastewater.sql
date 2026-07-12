-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "treatment_plant",
    "type_of_treatment",
    "hydraulic_design_capacity_1_000_m3_day",
    "amount_of_wastewater_received_1_000_m3_year",
    "amount_of_wastewater_received_1_000_m3_day"
FROM "qatar-planning-and-statistics-authority-urban-wastewater-treatment-plants-by-type-of-treatment-design-capacity-and-amount-of-wastewater"
