-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "quarter",
    "lrb",
    "age_group_of_mother_in_years",
    "fy_mr_l_m",
    "qataris",
    "qtry",
    "non_qataris",
    "gyr_qtry",
    "total",
    "ljmly"
FROM "qatar-planning-and-statistics-authority-registered-live-births-by-nationality-and-age-group-of-mother"
