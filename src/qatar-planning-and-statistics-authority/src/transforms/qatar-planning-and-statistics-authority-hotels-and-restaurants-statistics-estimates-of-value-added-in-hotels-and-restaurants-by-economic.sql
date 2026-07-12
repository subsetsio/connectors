-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "main_economic_activity",
    "net_value_added_value_in_1_000_qr_lqym_lmdf_lsfy_lqym_b_lf_ryl_qtry",
    "depreciations_value_in_1_000_qr_lhtlkt_lqym_b_lf_ryl_qtry",
    "gross_value_added_value_in_1_000_qr_lqym_lmdf_ljmly_lqym_b_lf_ryl_qtry",
    "intermediate_goods_and_services_value_value_in_1_000_qr_qym_lsl_wlkhdmt_lwsyt_lqym_b_lf_ryl_qtry",
    "production_value_value_in_1_000_qr_qym_lntj_lqym_b_lf_ryl_qtry",
    "lnsht_lqtsdy_lry_ysy"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-estimates-of-value-added-in-hotels-and-restaurants-by-economic"
