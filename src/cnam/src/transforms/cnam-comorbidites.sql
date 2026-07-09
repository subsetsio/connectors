-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: One row per (year, index pathology `top`, comorbid pathology). `ntop` repeats the index pathology's patient count on every comorbidity row — summing `ncomorb` or `ntop` across rows double-counts patients.
-- caution: `top` and the comorbidity columns span several levels of the pathology hierarchy (patho_niv1/2/3); rows at different levels overlap, so never sum across levels.
SELECT
    "annee",
    "patho_niv1",
    "patho_niv2",
    "patho_niv3",
    "top",
    "comorbidite",
    "libelle_comorbidite",
    "region",
    "dept",
    "ncomorb",
    "ntop",
    "proportion_comorb",
    "patho_niv1_comorb",
    "patho_niv2_comorb",
    "patho_niv3_comorb",
    "niveau_prioritaire"
FROM "cnam-comorbidites"
