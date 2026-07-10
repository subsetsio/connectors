-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "PROVNUM" AS provnum,
    "PROVNAME" AS provname,
    "CITY" AS city,
    "STATE" AS state,
    "COUNTY_NAME" AS county_name,
    "COUNTY_FIPS" AS county_fips,
    "CY_Qtr" AS cy_qtr,
    strptime("WorkDate", '%Y%m%d')::DATE AS workdate,
    CAST("MDScensus" AS BIGINT) AS mdscensus,
    CAST("Hrs_RNDON" AS DOUBLE) AS hrs_rndon,
    CAST("Hrs_RNDON_emp" AS DOUBLE) AS hrs_rndon_emp,
    CAST("Hrs_RNDON_ctr" AS DOUBLE) AS hrs_rndon_ctr,
    CAST("Hrs_RNadmin" AS DOUBLE) AS hrs_rnadmin,
    CAST("Hrs_RNadmin_emp" AS DOUBLE) AS hrs_rnadmin_emp,
    CAST("Hrs_RNadmin_ctr" AS DOUBLE) AS hrs_rnadmin_ctr,
    CAST("Hrs_RN" AS DOUBLE) AS hrs_rn,
    CAST("Hrs_RN_emp" AS DOUBLE) AS hrs_rn_emp,
    CAST("Hrs_RN_ctr" AS DOUBLE) AS hrs_rn_ctr,
    CAST("Hrs_LPNadmin" AS DOUBLE) AS hrs_lpnadmin,
    CAST("Hrs_LPNadmin_emp" AS DOUBLE) AS hrs_lpnadmin_emp,
    CAST("Hrs_LPNadmin_ctr" AS DOUBLE) AS hrs_lpnadmin_ctr,
    CAST("Hrs_LPN" AS DOUBLE) AS hrs_lpn,
    CAST("Hrs_LPN_emp" AS DOUBLE) AS hrs_lpn_emp,
    CAST("Hrs_LPN_ctr" AS DOUBLE) AS hrs_lpn_ctr,
    CAST("Hrs_CNA" AS DOUBLE) AS hrs_cna,
    CAST("Hrs_CNA_emp" AS DOUBLE) AS hrs_cna_emp,
    CAST("Hrs_CNA_ctr" AS DOUBLE) AS hrs_cna_ctr,
    CAST("Hrs_NAtrn" AS DOUBLE) AS hrs_natrn,
    CAST("Hrs_NAtrn_emp" AS DOUBLE) AS hrs_natrn_emp,
    CAST("Hrs_NAtrn_ctr" AS DOUBLE) AS hrs_natrn_ctr,
    CAST("Hrs_MedAide" AS DOUBLE) AS hrs_medaide,
    CAST("Hrs_MedAide_emp" AS DOUBLE) AS hrs_medaide_emp,
    CAST("Hrs_MedAide_ctr" AS DOUBLE) AS hrs_medaide_ctr
FROM "cms-7e0d53ba-8f02-4c66-98a5-14a1c997c50d"
