-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("WAC" AS BIGINT) AS wac,
    CAST("WAC_SEQ_ID2" AS BIGINT) AS wac_seq_id2,
    "WAC_NAME" AS wac_name,
    "WORLD_AREA_NAME" AS world_area_name,
    "COUNTRY_SHORT_NAME" AS country_short_name,
    "COUNTRY_TYPE" AS country_type,
    "CAPITAL" AS capital,
    "SOVEREIGNTY" AS sovereignty,
    "COUNTRY_CODE_ISO" AS country_code_iso,
    "STATE_CODE" AS state_code,
    "STATE_NAME" AS state_name,
    "STATE_FIPS" AS state_fips,
    "START_DATE" AS start_date,
    "THRU_DATE" AS thru_date,
    "COMMENTS" AS comments,
    CAST("IS_LATEST" AS BIGINT) AS is_latest
FROM "bts-gei"
