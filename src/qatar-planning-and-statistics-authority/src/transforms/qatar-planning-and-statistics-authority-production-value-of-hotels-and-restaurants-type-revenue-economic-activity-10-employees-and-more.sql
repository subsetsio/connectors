-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "type_of_revenue",
    "main_economic_activity",
    "production_value_value_in_1_000_qr_qym_lntj_lqym_b_lf_ryl_qtry",
    "lnsht_lqtsdy_lry_ysy",
    "nw_lyrdt"
FROM "qatar-planning-and-statistics-authority-production-value-of-hotels-and-restaurants-type-revenue-economic-activity-10-employees-and-more"
