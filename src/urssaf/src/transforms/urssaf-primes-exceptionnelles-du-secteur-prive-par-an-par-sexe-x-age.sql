-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "libelle_de_l_age",
    "libelle_du_sexe",
    "annee",
    "tranche_age",
    CAST("sexe" AS BIGINT) AS sexe,
    "total_individus_primes",
    "montant_di_total_primes",
    "montant_primes_moyen_par_indiv",
    "taux_de_couverture_des_di"
FROM "urssaf-primes-exceptionnelles-du-secteur-prive-par-an-par-sexe-x-age"
