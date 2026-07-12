-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "trtyb_lmwlwd",
    "birth_order",
    "md_lhy_lzwjy_blsnwt",
    "duration_of_marriage_in_years",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-duration-of-marriage-and-birth-order-qataris"
