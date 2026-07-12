-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "champ",
    "annee",
    "montant_prime_pepa",
    "montant_prime_covid",
    "total_montant_primes",
    "nombre_etablissement_prime_pepa",
    "nombre_etablissement_prime_covid",
    "total_etablissement_primes",
    "taux_de_couverture_des_di"
FROM "urssaf-primes-exceptionnelles-par-an-champ-large-france-entiere"
