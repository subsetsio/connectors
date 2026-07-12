-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "revenue_item",
    "main_activity",
    "revenues_from_current_activity_value_in_1_000_qr_yrdt_lnsht_ljry_lqym_b_lf_ryl_qtry",
    "lnsht_lry_ysy",
    "bnd_lyrdt"
FROM "qatar-planning-and-statistics-authority-revenues-hotels-restaurants-current-activity-by-revenue-item-and-main-activity-10-employees-and-more"
