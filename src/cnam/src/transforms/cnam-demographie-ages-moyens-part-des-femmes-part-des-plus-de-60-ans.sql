-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: National-level only (no territory dimension). `profession_sante` includes an all-professions aggregate alongside individual professions.
-- caution: All measures are shares or mean ages — averaging or summing them across professions without weighting by headcount is invalid.
-- caution: `vision_*` flags are display flags of the profession, not data dimensions.
SELECT
    "annee",
    "profession_sante",
    "part_femmes",
    "part_hommes",
    "part_des_60_ans_et_plus",
    "part_des_moins_de_60_ans",
    "age_moyen_global",
    "age_moyen_femmes",
    "age_moyen_hommes",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire"
FROM "cnam-demographie-ages-moyens-part-des-femmes-part-des-plus-de-60-ans"
