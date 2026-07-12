-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "details",
    "ltfsyl",
    "2022_q4",
    "2023_q3",
    "2023_q4",
    "change_y_o_y",
    "change_q_o_q"
FROM "qatar-planning-and-statistics-authority-total-imports-by-main-country-of-origin-q4-20230"
