-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "quarter",
    "lrb_lsnwy",
    "nationality",
    "ljnsy",
    "gender",
    "lnw",
    "age_group",
    "lfy_l_mry",
    "number_of_economically_inactive_population_dd_lskn_gyr_lnshytyn_qtsdyan"
FROM "qatar-planning-and-statistics-authority-labor-force-statistics-number-of-economically-inactive-population-aged-15-years-and-above-by-quarter"
