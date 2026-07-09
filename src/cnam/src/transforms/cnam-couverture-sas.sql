-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The territory columns mix levels: département rows, région rows and a national row coexist. Filter before aggregating; `taux_population_couverte` is a percentage and must never be summed.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    CAST("taux_population_couverte" AS DOUBLE) AS taux_population_couverte,
    "couvert",
    "taux_population_couverte_integer"
FROM "cnam-couverture-sas"
