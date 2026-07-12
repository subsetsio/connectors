-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "revenue_item",
    "main_activity",
    "transformational_revenues_value_in_1_000_qr_lyrdt_lthwyly_lqym_b_lf_ryl_qtry",
    "lnsht_lry_ysy",
    "bnwd_lyrdt_l_khr"
FROM "qatar-planning-and-statistics-authority-transformational-revenues-by-revenue-item-and-main-activity-establishments-with-10-employees-or-more"
