-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "electricity_power_generation_from_wte_mwh",
    "compost_including_pre_screened_compost_tons",
    "biogas_1000_m3"
FROM "qatar-planning-and-statistics-authority-production-capacity-of-solid-waste-management-center-in-mesaieed-by-type"
