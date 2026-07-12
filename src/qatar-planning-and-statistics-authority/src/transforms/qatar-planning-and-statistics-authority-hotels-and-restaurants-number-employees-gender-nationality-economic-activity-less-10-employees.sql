-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "activity_code_rmz_lnsht",
    "gender",
    "nationality",
    "main_economic_activity",
    "number_of_employees_dd_lmshtglyn",
    "lnw",
    "ljnsy",
    "lnsht_lqtsdy_lry_ysy"
FROM "qatar-planning-and-statistics-authority-hotels-and-restaurants-number-employees-gender-nationality-economic-activity-less-10-employees"
