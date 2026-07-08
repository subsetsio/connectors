SELECT
    INDICATOR                                    AS indicator,
    ECONOMY_CODE                                 AS economy_code,
    CAST(TIME_PERIOD AS INTEGER)                 AS year,
    CAST(OBS_VALUE AS DOUBLE)                    AS value,
    NULLIF(UNIT, '')                             AS unit,
    TRY_CAST(NULLIF(UNIT_MULT, '') AS INTEGER)   AS unit_mult,
    TRY_CAST(NULLIF(DECIMALS, '') AS INTEGER)    AS decimals,
    NULLIF(OBS_STATUS, '')                       AS obs_status,
    NULLIF(REF_YEAR, '')                         AS ref_year,
    NULLIF(BASE_YEAR, '')                        AS base_year,
    NULLIF(DATA_SOURCE, '')                      AS data_source,
    NULLIF(METHODOLOGY, '')                      AS methodology,
    NULLIF(FOOTNOTE, '')                         AS footnote
FROM "adb-ppl-le"
WHERE OBS_VALUE IS NOT NULL
  AND OBS_VALUE <> ''
  AND TRY_CAST(OBS_VALUE AS DOUBLE) IS NOT NULL
