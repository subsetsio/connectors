-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "size_of_establishment",
    "main_economic_activity",
    "number_of_employees_dd_lmshtglyn",
    "number_of_establishments_dd_lmnshat",
    "lnsht_lqtsdy_lry_ysy",
    "hjm_lmnsh"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-number-establishments-employees-by-size-of-establishment-economic-activity"
