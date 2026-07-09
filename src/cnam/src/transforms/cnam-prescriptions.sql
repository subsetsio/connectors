-- Published pass-through of raw asset `cnam-prescriptions`.
-- French-formatted measure strings are dropped for their parsed numeric twins; the `vision_*` portal flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "poste_prescription" AS prescription_post_code,
    "libelle_poste_prescription" AS prescription_post,
    "montant_total_prescription_integer" AS total_prescription_amount_eur,
    "montant_moyen_prescription_integer" AS mean_prescription_amount_eur
FROM "cnam-prescriptions"
