-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Prscrbr_NPI" AS BIGINT) AS prscrbr_npi,
    "Prscrbr_Last_Org_Name" AS prscrbr_last_org_name,
    "Prscrbr_First_Name" AS prscrbr_first_name,
    "Prscrbr_City" AS prscrbr_city,
    "Prscrbr_State_Abrvtn" AS prscrbr_state_abrvtn,
    "Prscrbr_State_FIPS" AS prscrbr_state_fips,
    "Prscrbr_Type" AS prscrbr_type,
    "Prscrbr_Type_Src" AS prscrbr_type_src,
    "Brnd_Name" AS brnd_name,
    "Gnrc_Name" AS gnrc_name,
    CAST("Tot_Clms" AS BIGINT) AS tot_clms,
    CAST("Tot_30day_Fills" AS BIGINT) AS tot_30day_fills,
    CAST("Tot_Day_Suply" AS BIGINT) AS tot_day_suply,
    CAST("Tot_Drug_Cst" AS DOUBLE) AS tot_drug_cst,
    "Tot_Benes" AS tot_benes,
    "GE65_Sprsn_Flag" AS ge65_sprsn_flag,
    "GE65_Tot_Clms" AS ge65_tot_clms,
    "GE65_Tot_30day_Fills" AS ge65_tot_30day_fills,
    "GE65_Tot_Drug_Cst" AS ge65_tot_drug_cst,
    "GE65_Tot_Day_Suply" AS ge65_tot_day_suply,
    "GE65_Bene_Sprsn_Flag" AS ge65_bene_sprsn_flag,
    "GE65_Tot_Benes" AS ge65_tot_benes
FROM "cms-9552739e-3d05-4c1b-8eff-ecabf391e2e5"
