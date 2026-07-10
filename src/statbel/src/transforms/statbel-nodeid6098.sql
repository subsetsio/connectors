-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The raw file has no scan-verified non-null row key; treat rows as source observations and avoid assuming row identity beyond the full record.
-- caution: Geographic and demographic dimensions may include aggregate categories alongside detailed categories; filter dimensions before summing.
SELECT
    "TX_CANTON" AS tx_canton,
    "MS_ADDRESS" AS ms_address,
    "DT_DATE" AS dt_date,
    CAST("MS_POPULATION" AS BIGINT) AS ms_population,
    CAST("MS_MALE" AS BIGINT) AS ms_male,
    CAST("MS_FEMALE" AS BIGINT) AS ms_female,
    CAST("MS_Y_0_14" AS BIGINT) AS ms_y_0_14,
    CAST("MS_Y_15_64" AS BIGINT) AS ms_y_15_64,
    CAST("MS_Y__65" AS BIGINT) AS ms_y_65
FROM "statbel-nodeid6098"
