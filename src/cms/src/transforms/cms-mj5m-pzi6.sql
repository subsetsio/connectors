-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "Ind_PAC_ID" AS ind_pac_id,
    "Ind_enrl_ID" AS ind_enrl_id,
    "Provider Last Name" AS provider_last_name,
    "Provider First Name" AS provider_first_name,
    "Provider Middle Name" AS provider_middle_name,
    "suff",
    "gndr",
    "Cred" AS cred,
    "Med_sch" AS med_sch,
    "Grd_yr" AS grd_yr,
    "pri_spec",
    "sec_spec_1",
    "sec_spec_2",
    "sec_spec_3",
    "sec_spec_4",
    "sec_spec_all",
    "Telehlth" AS telehlth,
    "Facility Name" AS facility_name,
    "org_pac_id",
    "num_org_mem",
    "adr_ln_1",
    "adr_ln_2",
    "ln_2_sprs",
    "City/Town" AS city_town,
    "State" AS state,
    "ZIP Code" AS zip_code,
    "Telephone Number" AS telephone_number,
    "ind_assgn",
    "grp_assgn",
    "adrs_id"
FROM "cms-mj5m-pzi6"
