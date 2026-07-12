-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "trtyb_lmwlwd",
    "birth_order",
    "fy_mr_l_m_blsnwt",
    "mother_s_age_group_in_years",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-mother-s-age-group-and-birth-order-qataris"
