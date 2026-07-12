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
    "bnd_lyrdt"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-transformational-revenues-by-revenue-item-and-main-activity0"
