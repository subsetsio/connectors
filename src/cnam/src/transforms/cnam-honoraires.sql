-- Published pass-through of raw asset `cnam-honoraires`.
-- French-formatted measure strings are dropped for their parsed numeric twins; `taux_depassement` (constant `non`) and the `vision_*` portal flags are dropped.
SELECT
    CAST(EXTRACT(YEAR FROM "annee") AS BIGINT) AS year,
    "profession_sante" AS profession,
    "region" AS region_code,
    "libelle_region" AS region_name,
    "departement" AS department_code,
    "libelle_departement" AS department_name,
    "totaux_integer" AS fees_total_eur,
    "moyens_integer" AS fees_mean_eur,
    "hono_sans_depassement_totaux_integer" AS fees_excl_extra_billing_total_eur,
    "hono_sans_depassement_moyens_integer" AS fees_excl_extra_billing_mean_eur,
    "depassements_totaux_integer" AS extra_billing_total_eur,
    "depassements_moyens_integer" AS extra_billing_mean_eur,
    "taux_depassement_s2_integer" AS extra_billing_rate_sector_2_pct,
    "taux_depassement_s2_optam_integer" AS extra_billing_rate_sector_2_optam_pct,
    "taux_depassement_s2_non_optam_integer" AS extra_billing_rate_sector_2_non_optam_pct
FROM "cnam-honoraires"
