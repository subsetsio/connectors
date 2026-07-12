-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "tranche_age",
    "libelle_de_l_age",
    CAST("sexe" AS BIGINT) AS sexe,
    "libelle_du_sexe",
    "secteur_na38",
    "grand_secteur_d_activite",
    "nature_de_contrat",
    "duree_de_contrat",
    "dpae_brut"
FROM "urssaf-dpae-annuelles-sexe-age"
