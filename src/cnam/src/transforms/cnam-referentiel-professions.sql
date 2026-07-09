-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `vision_*` and `menu` columns are display flags controlling where a profession appears on the CNAM portal, not properties of the profession itself.
SELECT
    "profession_sante",
    "tri",
    "vision_generale_all",
    "vision_generale_prescriptions",
    "vision_profession_territoire",
    "menu",
    "taux_depassement",
    "vision_honoraires_actes_niveau_2",
    "vision_honoraires_remunerations_niveau_2",
    "vision_honoraires_actescliniques_niveau_3",
    "vision_honoraires_actestechniques_niveau_3",
    "column_11"
FROM "cnam-referentiel-professions"
