-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "type_of_service",
    "main_economic_activity",
    "estimates_of_intermediate_services_value_value_in_1_000_qr_tqdyrt_qym_lkhdmt_lwsyt_lqym_b_lf_ryl_qtr",
    "lnsht_lqtsdy_lry_ysy",
    "nw_lkhdm"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-estimates-of-intermediate-services-value-in-hotels-and-restaurants0"
