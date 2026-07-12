-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("month_year", '%Y-%m')::DATE AS month_year,
    "fog_vis_1_k_m",
    "dust_storm_vis_1_k_m",
    "haze_vis_5_k_m"
FROM "qatar-planning-and-statistics-authority-fog-dust-storm-and-haze-doha-international-airport-2011-2024"
