-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "category",
    "lfy",
    "2022_q4",
    "2023_q3",
    "2023_q4",
    "change_y_o_y_nsb_ltgyyr_lsnwy",
    "change_q_o_q_nsb_ltgyyr_lrb_y"
FROM "qatar-planning-and-statistics-authority-total-imports-by-sections-of-sitc-2023-q4"
