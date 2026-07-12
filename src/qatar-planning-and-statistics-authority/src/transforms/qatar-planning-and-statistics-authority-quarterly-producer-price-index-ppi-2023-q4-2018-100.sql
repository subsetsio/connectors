-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "economic_activity_product",
    "lnsht_lqtsdy_lmntj",
    "weight",
    "2022_q4",
    "2023_q3",
    "2023_q4",
    "change_y_o_y_nsb_ltgyyr_lsnwy",
    "change_q_o_q_nsb_ltgyyr_lrb_y"
FROM "qatar-planning-and-statistics-authority-quarterly-producer-price-index-ppi-2023-q4-2018-100"
