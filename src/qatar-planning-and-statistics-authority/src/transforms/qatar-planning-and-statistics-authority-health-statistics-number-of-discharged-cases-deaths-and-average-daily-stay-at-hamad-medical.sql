-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year_lsn",
    "international_classification_of_diseases_code_rmz_ltsnyf_ldwly_ll_mrd",
    "type_of_disease",
    "type_of_disease_ar",
    "average_daily_stay_mtwst_lqm_lywmy",
    "number_of_deaths_dd_lwfyt",
    "number_of_discharged_cases_dd_lmrd_ldhyn_tm_khrjh_mn_lmstshf"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-of-discharged-cases-deaths-and-average-daily-stay-at-hamad-medical"
