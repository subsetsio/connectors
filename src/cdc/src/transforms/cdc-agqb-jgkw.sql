-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEO_ID" AS geo_id,
    CAST("STATE" AS BIGINT) AS state,
    CAST("COUNTY" AS BIGINT) AS county,
    CAST("TRACT" AS BIGINT) AS tract,
    CAST("CT_Fips" AS BIGINT) AS ct_fips,
    CAST("CFLD_AFREQ" AS DOUBLE) AS cfld_afreq,
    CAST("DRGT_AFREQ" AS DOUBLE) AS drgt_afreq,
    CAST("HRCN_AFREQ" AS DOUBLE) AS hrcn_afreq,
    CAST("RFLD_AFREQ" AS DOUBLE) AS rfld_afreq,
    CAST("WFIR_AFREQ" AS DOUBLE) AS wfir_afreq,
    CAST("SPL_THEMES" AS DOUBLE) AS spl_themes,
    CAST("state_SPL_THEMES" AS DOUBLE) AS state_spl_themes,
    CAST("IntersectArea_wellpop" AS DOUBLE) AS intersectarea_wellpop,
    CAST("IntersectArea_no3_conc" AS DOUBLE) AS intersectarea_no3_conc,
    CAST("IntersectArea_BRT10prob" AS DOUBLE) AS intersectarea_brt10prob,
    CAST("tot" AS BIGINT) AS tot,
    CAST("hisp_tot" AS BIGINT) AS hisp_tot,
    CAST("white_nh_tot" AS BIGINT) AS white_nh_tot,
    CAST("black_nh_tot" AS BIGINT) AS black_nh_tot,
    CAST("native_nh_tot" AS BIGINT) AS native_nh_tot,
    CAST("asian_nh_tot" AS BIGINT) AS asian_nh_tot,
    CAST("pi_nh_tot" AS BIGINT) AS pi_nh_tot,
    CAST("other_nh_tot" AS BIGINT) AS other_nh_tot,
    CAST("twoplus_nh_tot" AS BIGINT) AS twoplus_nh_tot,
    CAST("male_tot" AS BIGINT) AS male_tot,
    CAST("female_tot" AS BIGINT) AS female_tot,
    CAST("a_under_5" AS BIGINT) AS a_under_5,
    CAST("a_5to24" AS BIGINT) AS a_5to24,
    CAST("a_25to64" AS BIGINT) AS a_25to64,
    CAST("a_65up" AS BIGINT) AS a_65up,
    "Climate_regions" AS climate_regions
FROM "cdc-agqb-jgkw"
