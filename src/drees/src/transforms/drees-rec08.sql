-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "annee",
    "sexe",
    "variable",
    "intitule",
    "retraites_nes_a_l_etranger_et_residents_a_l_etranger",
    "retraites_nes_a_l_etranger_et_residents_en_france",
    "retraites_nes_en_france_et_residents_a_l_etranger",
    "retraites_nes_en_france_et_residents_en_france",
    "retraites_nes_a_l_etranger",
    "retraites_nes_en_france",
    "retraites_residents_a_l_etranger",
    "retraites_residents_en_france",
    "ensemble"
FROM "drees-rec08"
