-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "main_economic_activity",
    "number_of_employees_dd_lmshtglyn",
    "compensations_of_employees_t_wydt_l_mlyn_qr_000",
    "nationality",
    "main_economic_activity_ar",
    "nationality_ar"
FROM "qatar-planning-and-statistics-authority-employee-count-and-compensation-estimates-by-nationality-and-economic-activity-isic-rev4-codes-4922-6190-under-10-employees"
