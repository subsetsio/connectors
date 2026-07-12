-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "annee",
    "montant_prime_pepa",
    "montant_prime_covid",
    "total_montant_primes",
    "nombre_etablissement_prime_pepa",
    "nombre_etablissement_prime_covid",
    "total_etablissement_primes",
    "total_etablissements_actifs",
    "part_etablissements_avec_primes",
    "nombre_individus_prime_pepa",
    "nombre_individus_prime_covid",
    "total_individus_primes",
    "montant_di_pepa",
    "montant_di_prime_covid",
    "montant_di_total_primes",
    "montant_pepa_moyen_par_indiv",
    "mtt_prime_covid_moyen_par_indiv",
    "montant_primes_moyen_par_indiv",
    "taux_de_couverture_des_di"
FROM "urssaf-primes-exceptionnelles-du-secteur-prive-par-an-france-entiere"
