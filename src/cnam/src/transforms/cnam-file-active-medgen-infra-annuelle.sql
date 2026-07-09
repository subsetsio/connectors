-- Published pass-through of raw asset `cnam-file-active-medgen-infra-annuelle`.
-- `nombre_patients_uniques` has no parsed twin in this export; it is TRY_CAST, so the source's NS/NC sentinels become nulls.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    TRY_CAST("nombre_patients_uniques" AS BIGINT) AS mean_unique_patients,
    "taux_evolution_annuel_integer" AS annual_change_pct
FROM "cnam-file-active-medgen-infra-annuelle"
