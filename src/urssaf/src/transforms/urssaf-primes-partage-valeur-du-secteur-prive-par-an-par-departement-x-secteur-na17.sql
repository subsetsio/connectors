-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "departement",
    "region",
    "ancienne_region",
    "secteur_na17i",
    "grand_secteur_d_activite",
    "annee",
    "code_region",
    "code_ancienne_region",
    "code_departement",
    "nombre_etablissement_prime_ppv",
    "total_etablissements_actifs",
    "part_etablissements_avec_primes",
    "nombre_individus_prime_ppv",
    "montant_prime_ppv",
    "montant_ppv_moyen_par_indiv",
    "montant_di_total_ppv",
    "taux_de_couverture_des_di"
FROM "urssaf-primes-partage-valeur-du-secteur-prive-par-an-par-departement-x-secteur-na17"
