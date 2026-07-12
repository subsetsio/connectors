-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnsht_lqtsdy",
    "economic_activity",
    "kmy_myh_ltbryd_lt_wydy_lmstkhdm_hsb_lmsdr_m3",
    "quantity_of_compensatory_cooling_water_used_by_source_m3",
    "value"
FROM "qatar-planning-and-statistics-authority-district-cooling-plants-by-economic-activity-water-source-and-quantity-used-m3"
