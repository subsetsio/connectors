-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "nombre_d_etablissements_en_france_metropolitaine_au_31_decembre",
    "nombre_de_naissances_vivantes_en_france_metropolitaine",
    "nombre_d_etablissements_en_france_entiere_au_31_decembre",
    "nombre_de_naissances_vivantes_en_france_entiere"
FROM "drees-datastory-maternites-graphique-1"
