-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "secteur_na38i",
    "grand_secteur_d_activite",
    "annee",
    "trimestre",
    "dernier_jour_du_trimestre",
    "total_montant_primes",
    "total_etablissement_primes",
    "total_etablissements_actifs",
    "part_etablissements_avec_primes",
    "total_individus_primes",
    "montant_di_total_primes",
    "montant_primes_moyen_par_indiv",
    "taux_de_couverture_des_di"
FROM "urssaf-primes-exceptionnelles-du-secteur-prive-par-trimestre-france-x-secteur-na38"
