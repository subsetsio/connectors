-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "sexe",
    "regime",
    "pension_moyenne_des_invalides_de_categorie_1",
    "pension_moyenne_des_invalides_de_categorie_2",
    "pension_moyenne_des_invalides_de_categorie_3",
    "pension_moyenne_des_autres_invalides_de_droits_directs",
    "pension_d_invalidite_de_droits_directs_moyenne"
FROM "drees-invalidite-pensmoy-dd"
