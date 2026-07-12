-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "activity",
    "activity_ar",
    "15_qatari_male",
    "15_qatari_female",
    "15_non_qatari_male",
    "15_non_qatari_female",
    "15_19_qatari_male",
    "15_19_qatari_female",
    "15_19_non_qatari_male",
    "15_19_non_qatari_female",
    "20_24_qatari_male",
    "20_24_qatari_female",
    "20_24_non_qatari_male",
    "20_24_non_qatari_female",
    "25_qatari_male",
    "25_qatari_female",
    "25_non_qatari_male",
    "25_non_qatari_female",
    "total_qatari_male",
    "total_qatari_female",
    "total_non_qatari_male",
    "total_non_qatari_female"
FROM "qatar-planning-and-statistics-authority-participants-in-youth-and-sports-institutions-by-activity-age-nationality-and-gender-2023-copy"
