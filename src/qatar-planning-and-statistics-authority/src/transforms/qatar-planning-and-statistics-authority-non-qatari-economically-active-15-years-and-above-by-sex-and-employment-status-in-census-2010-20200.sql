-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "employment_status",
    "lhl_l_mly",
    "sex",
    "ljns",
    "2010",
    "20100",
    "2020",
    "20200",
    "change_nsb_ltgyyr"
FROM "qatar-planning-and-statistics-authority-non-qatari-economically-active-15-years-and-above-by-sex-and-employment-status-in-census-2010-20200"
