-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "annee",
    "nombre_etablissement_prime_ppv",
    "total_etablissements_actifs",
    "part_etablissements_avec_primes",
    "nombre_individus_prime_ppv",
    "montant_prime_ppv",
    "montant_ppv_moyen_par_indiv",
    "montant_di_total_ppv",
    "taux_de_couverture_des_di"
FROM "urssaf-prime-partage-valeur-par-an-champ-large-france-entiere"
