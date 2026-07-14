-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Market-potential source files carry different access concepts; filter by source_file before comparing values.
SELECT
    "source_file,iso,year,RMP_RV,FMP_RV,RMP_HM,FMP_HM,RMP_IV1,RMP_IV2,gdpcap,avgyrs,lrmp_rv,lfmp_rv,lrmp_hm,lfmp_hm,lrmp_iv1,lrmp_iv2,lgcap" AS source_file_iso_year_rmp_rv_fmp_rv_rmp_hm_fmp_hm_rmp_iv1_rmp_iv2_gdpcap_avgyrs_lrmp_rv_lfmp_rv_lrmp_hm_lfmp_hm_lrmp_iv1_lrmp_iv2_lgcap
FROM "cepii-market-potentials"
