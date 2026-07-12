-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "marital_status",
    "lhl_ljtm_y",
    "gender",
    "lnw",
    "percentage_of_qataris",
    "total_qataris_census_2010",
    "total_qataris_census_2020",
    "percentage_change"
FROM "qatar-planning-and-statistics-authority-qatari-marital-status-15-years-and-above-by-sex-in-census-2010-2020"
