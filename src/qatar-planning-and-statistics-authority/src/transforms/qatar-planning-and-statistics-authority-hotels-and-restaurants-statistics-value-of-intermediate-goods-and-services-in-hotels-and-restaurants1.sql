-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "type",
    "main_economic_activity",
    "value_value_in_1_000_qr_lqym_lqym_b_lf_ryl_qtry",
    "lnsht_lqtsdy_lry_ysy",
    "lnw"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-statistics-value-of-intermediate-goods-and-services-in-hotels-and-restaurants1"
