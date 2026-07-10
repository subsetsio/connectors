-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("Year" AS BIGINT) AS year,
    "quarter",
    "Bene_Geo_Desc" AS bene_geo_desc,
    "Bene_Mdcd_Mdcr_Enrl_Stus" AS bene_mdcd_mdcr_enrl_stus,
    "Bene_Race_Desc" AS bene_race_desc,
    "Bene_Sex_Desc" AS bene_sex_desc,
    "Bene_Mdcr_Entlmt_Stus" AS bene_mdcr_entlmt_stus,
    "Bene_Age_Desc" AS bene_age_desc,
    "Bene_RUCA_Desc" AS bene_ruca_desc,
    "Total_Bene_TH_Elig" AS total_bene_th_elig,
    "Total_PartB_Enrl" AS total_partb_enrl,
    "Total_Bene_Telehealth" AS total_bene_telehealth,
    "Pct_Telehealth" AS pct_telehealth
FROM "cms-939226be-b107-476e-8777-f199a840138a"
