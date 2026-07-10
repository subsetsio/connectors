-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    CAST("col_0" AS BIGINT) AS col_0,
    "global_sea",
    "SubCat" AS subcat,
    "cd_goods",
    CAST("cd_lod_type" AS BIGINT) AS cd_lod_type,
    CAST("EEA" AS BIGINT) AS eea,
    CAST("Tot_ms_wt_arriv" AS BIGINT) AS tot_ms_wt_arriv,
    CAST("Tot_ms_nb_arriv" AS BIGINT) AS tot_ms_nb_arriv,
    CAST("Tot_ms_wt_depart" AS BIGINT) AS tot_ms_wt_depart,
    CAST("Tot_ms_nb_depart" AS BIGINT) AS tot_ms_nb_depart
FROM "statbel-nodeid6608"
