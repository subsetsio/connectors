-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "mhn_l_b",
    "father_s_occupation",
    "ljnsy",
    "nationality",
    "fy_mr_l_b_blsnwt",
    "father_s_age_group_in_years",
    "value"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-father-s-age-group-nationality-and-occupation"
