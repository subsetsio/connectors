-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "lnfq_l_nsht_hmy_wdr_lbyy",
    "expenditures_on_environmental_protection_activities",
    "lfy_lfr_y_llnsht_lbyy_y",
    "environmental_activity_subcategory",
    "lnfqt",
    "expenditures",
    "value"
FROM "qatar-planning-and-statistics-authority-district-cooling-services-providers-expenditures-on-environmental-protection-activities-and-management-qr"
