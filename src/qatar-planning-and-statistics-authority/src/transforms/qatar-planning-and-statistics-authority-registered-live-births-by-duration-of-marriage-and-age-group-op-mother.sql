-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "age_group_of_mother",
    "fy_mr_l_m",
    "duration_of_marriage_years",
    "md_lzwj_blsnwt",
    "live_births",
    "lwldt_lhy"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-duration-of-marriage-and-age-group-op-mother"
