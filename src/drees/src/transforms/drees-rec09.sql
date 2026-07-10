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
    "retraites_beneficiaires_d_un_minimum_de_pension",
    "retraites_beneficiaires_d_un_minimum_de_pension_dans_leur_regime_principal",
    "retraites_beneficiaires_d_un_minimum_de_pension_dans_un_regime_secondaire",
    "retraites_non_beneficiaires_d_un_minimum_de_pension",
    "assures_beneficiaires_du_minimum_vieillesse",
    "assures_non_beneficiaires_du_minimum_vieillesse",
    "ensemble"
FROM "drees-rec09"
