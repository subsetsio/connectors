-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnsht_lqtsdy",
    "economic_activity",
    "slwb_ltkhls_mn_myh_mhtt_ltbryd_lmrfwd_hsb_lkmy_m3",
    "cooling_plant_disposal_method_by_quantity_m3",
    "value"
FROM "qatar-planning-and-statistics-authority-district-cooling-plants-by-economic-activity-and-disposal-method-for-rejected-cooling-water-m3"
