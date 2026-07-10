-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Sample #" AS BIGINT) AS sample,
    "PCR confirmed" AS pcr_confirmed,
    "Abbott Reactivity" AS abbott_reactivity,
    "Ortho Reactivity" AS ortho_reactivity,
    "In-House CDC ELISA Reactivity" AS in_house_cdc_elisa_reactivity,
    CAST("Abbott S/C Values" AS DOUBLE) AS abbott_s_c_values,
    CAST("Abbott S/C Values (Log10)" AS DOUBLE) AS abbott_s_c_values_log10,
    CAST("Ortho Index Values" AS DOUBLE) AS ortho_index_values,
    CAST("Ortho Index Values (Log10)" AS DOUBLE) AS ortho_index_values_log10,
    CAST("In-House CDC ELISA S/T Values" AS DOUBLE) AS in_house_cdc_elisa_s_t_values,
    CAST("In-House CDC ELISA S/T Values (Log10)" AS DOUBLE) AS in_house_cdc_elisa_s_t_values_log10,
    CAST("mNT TITER" AS BIGINT) AS mnt_titer,
    CAST("mNT TITER (Log10)" AS DOUBLE) AS mnt_titer_log10,
    CAST("sVNT % Inhibition" AS DOUBLE) AS svnt_inhibition
FROM "cdc-hhvg-83jq"
