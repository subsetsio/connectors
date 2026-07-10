-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This is a per-vessel-year table, not a static vessel master; vessel attributes and activity measures can vary by year and by the Global Fishing Watch flag and vessel class assignments.
SELECT
    CAST("mmsi" AS BIGINT) AS mmsi,
    "year",
    "flag_ais",
    "flag_registry",
    "flag_gfw",
    "vessel_class_inferred",
    "vessel_class_inferred_score",
    "vessel_class_registry",
    "vessel_class_gfw",
    "self_reported_fishing_vessel",
    "length_m_inferred",
    "length_m_registry",
    "length_m_gfw",
    "engine_power_kw_inferred",
    "engine_power_kw_registry",
    "engine_power_kw_gfw",
    "tonnage_gt_inferred",
    "tonnage_gt_registry",
    "tonnage_gt_gfw",
    "registries_listed",
    "active_hours",
    "fishing_hours"
FROM "global-fishing-watch-fishing-vessels"
