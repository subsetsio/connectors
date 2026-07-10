-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "Month" AS month,
    "Bene_Geo_Desc" AS bene_geo_desc,
    "Bene_Mdcd_Mdcr_Enrl_Stus" AS bene_mdcd_mdcr_enrl_stus,
    "Bene_Race_Desc" AS bene_race_desc,
    "Bene_Sex_Desc" AS bene_sex_desc,
    "Bene_Mdcr_Entlmt_Stus" AS bene_mdcr_entlmt_stus,
    "Bene_Age_Desc" AS bene_age_desc,
    "Bene_RUCA_Desc" AS bene_ruca_desc,
    "Total_Hosp" AS total_hosp,
    "Total_Enrl" AS total_enrl,
    "Total_Hosp_Per100K" AS total_hosp_per100k,
    "Avg_LOS" AS avg_los,
    "Pct_Dschrg_SNF" AS pct_dschrg_snf,
    "Pct_Dschrg_Expired" AS pct_dschrg_expired,
    "Pct_Dschrg_Home" AS pct_dschrg_home,
    "Pct_Dschrg_Hspc" AS pct_dschrg_hspc,
    "Pct_Dschrg_HomeHealth" AS pct_dschrg_homehealth,
    "Pct_Dschrg_Other" AS pct_dschrg_other
FROM "cms-2684c3e2-3598-4997-a598-0991bad6fbf2"
