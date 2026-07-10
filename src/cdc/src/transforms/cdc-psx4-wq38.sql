-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "GEOID" AS geoid,
    "NAME" AS name,
    "ST_GEOID" AS st_geoid,
    "ST_NAME" AS st_name,
    "Intent" AS intent,
    "Period" AS period,
    "Count" AS count,
    CAST("Rate" AS DOUBLE) AS rate,
    CAST("Rate_M" AS BIGINT) AS rate_m,
    "Rate_M_CI" AS rate_m_ci,
    strptime("Data_As_Of", '%m/%d/%Y')::DATE AS data_as_of,
    "TTM_Date_Range" AS ttm_date_range
FROM "cdc-psx4-wq38"
