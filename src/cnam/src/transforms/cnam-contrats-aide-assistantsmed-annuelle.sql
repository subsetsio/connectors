-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The territory columns mix levels: département rows, région rows and a national row coexist. Filter on the territory level before summing `nombre_contrat_assmed`.
SELECT
    CAST("annee" AS BIGINT) AS annee,
    "profession_sante_nbr_contrats",
    "profession_sante_taux",
    "region",
    "libelle_region",
    "departement",
    "libelle_departement",
    "nombre_contrat_assmed",
    "taux_adhesions",
    "taux_adhesions_integer"
FROM "cnam-contrats-aide-assistantsmed-annuelle"
