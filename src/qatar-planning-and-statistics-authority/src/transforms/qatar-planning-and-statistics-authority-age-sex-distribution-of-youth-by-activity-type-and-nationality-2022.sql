-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "activity_type",
    "sports_activity_ar",
    "15_qatari_m",
    "15_qatari_f",
    "15_non_qatari_m",
    "15_non_qatari_f",
    "15_19_qatari_m",
    "15_19_qatari_f",
    "15_19_non_qatari_m",
    "15_19_non_qatari_f",
    "20_24_qatari_m",
    "20_24_qatari_f",
    "20_24_non_qatari_m",
    "20_24_non_qatari_f",
    "25_qatari_m",
    "25_qatari_f",
    "25_non_qatari_m",
    "25_non_qatari_f",
    "total_qatari_m",
    "total_qatari_f",
    "total_non_qatari_m",
    "total_non_qatari_f",
    "grand_total"
FROM "qatar-planning-and-statistics-authority-age-sex-distribution-of-youth-by-activity-type-and-nationality-2022"
