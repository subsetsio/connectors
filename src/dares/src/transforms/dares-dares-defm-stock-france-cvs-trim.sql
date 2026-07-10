-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "date",
    "champ",
    "type_de_donnees",
    "categorie",
    "sexe",
    "tranche_d_age",
    "tranche_d_heures_travaillees",
    "anciennete",
    "nombre_de_demandeurs_d_emploi"
FROM "dares-dares-defm-stock-france-cvs-trim"
