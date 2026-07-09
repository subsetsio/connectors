-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A single in-progress-year snapshot (`annee` is constant, `date` is the end of the reference period), not a time series.
-- caution: The territory columns mix levels: département rows, région rows and a national row coexist. Filter before summing.
SELECT
    "annee",
    "date",
    "profession_sante_nbr_contrats",
    "profession_sante_taux",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_contrat_assmed",
    "taux_adhesions"
FROM "cnam-contrats-aide-assistantsmed-infra-annuelle"
