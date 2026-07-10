-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Ferret" AS ferret,
    "Virus" AS virus,
    CAST("inoc_dose" AS DOUBLE) AS inoc_dose,
    "units",
    "expt",
    CAST("lethal" AS BOOLEAN) AS lethal,
    CAST("lethal_day" AS BIGINT) AS lethal_day,
    CAST("NW_typical" AS BOOLEAN) AS nw_typical,
    "RD_trans" AS rd_trans,
    CAST("HPAI" AS BOOLEAN) AS hpai,
    CAST("HPAI_MBAA" AS BOOLEAN) AS hpai_mbaa,
    "HA" AS ha,
    "NA" AS na,
    "Origin" AS origin,
    CAST("wt_loss" AS DOUBLE) AS wt_loss,
    CAST("wt_loss_day" AS BIGINT) AS wt_loss_day,
    CAST("temp" AS DOUBLE) AS temp,
    CAST("temp_day" AS BIGINT) AS temp_day,
    CAST("temp_5" AS DOUBLE) AS temp_5,
    CAST("temp_5_day" AS BIGINT) AS temp_5_day,
    CAST("d1_inoc" AS DOUBLE) AS d1_inoc,
    CAST("d2_inoc" AS DOUBLE) AS d2_inoc,
    CAST("d3_inoc" AS DOUBLE) AS d3_inoc,
    CAST("d4_inoc" AS DOUBLE) AS d4_inoc,
    CAST("d5_inoc" AS DOUBLE) AS d5_inoc,
    CAST("d6_inoc" AS DOUBLE) AS d6_inoc,
    CAST("d7_inoc" AS DOUBLE) AS d7_inoc,
    CAST("d8_inoc" AS DOUBLE) AS d8_inoc,
    CAST("d9_inoc" AS DOUBLE) AS d9_inoc
FROM "cdc-cr56-k9wj"
