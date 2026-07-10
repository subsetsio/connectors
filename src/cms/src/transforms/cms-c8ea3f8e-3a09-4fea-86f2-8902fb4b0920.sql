-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "Prscrbr_Geo_Lvl" AS prscrbr_geo_lvl,
    "Prscrbr_Geo_Cd" AS prscrbr_geo_cd,
    "Prscrbr_Geo_Desc" AS prscrbr_geo_desc,
    "Brnd_Name" AS brnd_name,
    "Gnrc_Name" AS gnrc_name,
    CAST("Tot_Prscrbrs" AS BIGINT) AS tot_prscrbrs,
    CAST("Tot_Clms" AS BIGINT) AS tot_clms,
    CAST("Tot_30day_Fills" AS BIGINT) AS tot_30day_fills,
    CAST("Tot_Drug_Cst" AS DOUBLE) AS tot_drug_cst,
    "Tot_Benes" AS tot_benes,
    "GE65_Sprsn_Flag" AS ge65_sprsn_flag,
    "GE65_Tot_Clms" AS ge65_tot_clms,
    "GE65_Tot_30day_Fills" AS ge65_tot_30day_fills,
    "GE65_Tot_Drug_Cst" AS ge65_tot_drug_cst,
    "GE65_Bene_Sprsn_Flag" AS ge65_bene_sprsn_flag,
    "GE65_Tot_Benes" AS ge65_tot_benes,
    CAST("LIS_Bene_Cst_Shr" AS DOUBLE) AS lis_bene_cst_shr,
    CAST("NonLIS_Bene_Cst_Shr" AS DOUBLE) AS nonlis_bene_cst_shr,
    "Opioid_Drug_Flag" AS opioid_drug_flag,
    "Opioid_LA_Drug_Flag" AS opioid_la_drug_flag,
    "Antbtc_Drug_Flag" AS antbtc_drug_flag,
    "Antpsyct_Drug_Flag" AS antpsyct_drug_flag
FROM "cms-c8ea3f8e-3a09-4fea-86f2-8902fb4b0920"
