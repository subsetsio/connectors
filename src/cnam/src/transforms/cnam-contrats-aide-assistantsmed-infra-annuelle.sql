-- Published pass-through of raw asset `cnam-contrats-aide-assistantsmed-infra-annuelle`.
-- `profession_sante_nbr_contrats` / `profession_sante_taux` are constant (médecins) and are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "date" AS period_end,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "nombre_contrat_assmed" AS medical_assistant_contracts,
    "taux_adhesions" AS adhesion_rate_pct
FROM "cnam-contrats-aide-assistantsmed-infra-annuelle"
