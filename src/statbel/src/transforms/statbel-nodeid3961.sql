-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
SELECT
    "CD_TOPIC" AS cd_topic,
    CAST("CD_REFNIS" AS BIGINT) AS cd_refnis,
    "TX_REFNIS_DESCR_NL" AS tx_refnis_descr_nl,
    "TX_REFNIS_DESCR_FR" AS tx_refnis_descr_fr,
    "CD_BUFFER" AS cd_buffer,
    CAST("MS_POPULATION" AS BIGINT) AS ms_population,
    CAST("MS_NOT_LOC" AS BIGINT) AS ms_not_loc,
    CAST("MS_POP_IN" AS BIGINT) AS ms_pop_in,
    CAST("MS_MALE_IN" AS BIGINT) AS ms_male_in,
    CAST("MS_FEMALE_IN" AS BIGINT) AS ms_female_in,
    CAST("MS_Y_0_14" AS BIGINT) AS ms_y_0_14,
    CAST("MS_Y_15_64" AS BIGINT) AS ms_y_15_64,
    CAST("MS_65" AS BIGINT) AS ms_65,
    CAST("MS_PRCT_POP_IN" AS DOUBLE) AS ms_prct_pop_in,
    CAST("MS_PRCT_MALE_IN" AS DOUBLE) AS ms_prct_male_in,
    CAST("MS_PRCT_FEMALE_IN" AS DOUBLE) AS ms_prct_female_in,
    CAST("MS_PRCT_Y_0_14" AS DOUBLE) AS ms_prct_y_0_14,
    CAST("MS_PRCT_Y_15_64" AS DOUBLE) AS ms_prct_y_15_64,
    CAST("MS_PRCT_65" AS DOUBLE) AS ms_prct_65
FROM "statbel-nodeid3961"
