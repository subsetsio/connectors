-- begin/end timestamps are rebuilt from the YEARMONTH + DAY + TIME components,
-- not from the source's BEGIN_DATE_TIME/END_DATE_TIME strings: those carry a
-- 2-digit year ("28-APR-50 14:45:00") and cannot be disambiguated across the
-- 1950-2049 span the archive covers. TIME is HHMM with leading zeros stripped.
--
-- damage_*_usd decodes the magnitude suffix on the source's coded string
-- (H hundreds, K thousands, M millions, B billions, bare = dollars). A handful
-- of rows carry an unknown suffix ('?', 'T') and decode to NULL, keeping the
-- original code in damage_*_code.
SELECT
    CAST("EVENT_ID" AS BIGINT)                                          AS event_id,
    CAST("EPISODE_ID" AS BIGINT)                                        AS episode_id,
    strptime("BEGIN_YEARMONTH" || lpad("BEGIN_DAY", 2, '0')
             || lpad("BEGIN_TIME", 4, '0'), '%Y%m%d%H%M')               AS begin_date_time,
    strptime("END_YEARMONTH" || lpad("END_DAY", 2, '0')
             || lpad("END_TIME", 4, '0'), '%Y%m%d%H%M')                 AS end_date_time,
    "CZ_TIMEZONE"                                                       AS time_zone,
    CAST("YEAR" AS INTEGER)                                             AS year,
    "EVENT_TYPE"                                                        AS event_type,
    "STATE"                                                             AS state,
    CAST("STATE_FIPS" AS INTEGER)                                       AS state_fips,
    "CZ_TYPE"                                                           AS cz_type,
    CAST("CZ_FIPS" AS INTEGER)                                          AS cz_fips,
    "CZ_NAME"                                                           AS cz_name,
    "WFO"                                                               AS wfo,
    CAST("INJURIES_DIRECT" AS INTEGER)                                  AS injuries_direct,
    CAST("INJURIES_INDIRECT" AS INTEGER)                                AS injuries_indirect,
    CAST("DEATHS_DIRECT" AS INTEGER)                                    AS deaths_direct,
    CAST("DEATHS_INDIRECT" AS INTEGER)                                  AS deaths_indirect,
    "DAMAGE_PROPERTY"                                                   AS damage_property_code,
    TRY_CAST(regexp_extract("DAMAGE_PROPERTY", '^([0-9.]+)', 1) AS DOUBLE)
        * CASE upper(regexp_extract("DAMAGE_PROPERTY", '([A-Za-z?]?)$', 1))
              WHEN 'K' THEN 1e3 WHEN 'M' THEN 1e6 WHEN 'B' THEN 1e9
              WHEN 'H' THEN 1e2 WHEN '' THEN 1 ELSE NULL END            AS damage_property_usd,
    "DAMAGE_CROPS"                                                      AS damage_crops_code,
    TRY_CAST(regexp_extract("DAMAGE_CROPS", '^([0-9.]+)', 1) AS DOUBLE)
        * CASE upper(regexp_extract("DAMAGE_CROPS", '([A-Za-z?]?)$', 1))
              WHEN 'K' THEN 1e3 WHEN 'M' THEN 1e6 WHEN 'B' THEN 1e9
              WHEN 'H' THEN 1e2 WHEN '' THEN 1 ELSE NULL END            AS damage_crops_usd,
    CAST("MAGNITUDE" AS DOUBLE)                                         AS magnitude,
    "MAGNITUDE_TYPE"                                                    AS magnitude_type,
    "FLOOD_CAUSE"                                                       AS flood_cause,
    CAST("CATEGORY" AS INTEGER)                                         AS hurricane_category,
    "TOR_F_SCALE"                                                       AS tor_f_scale,
    CAST("TOR_LENGTH" AS DOUBLE)                                        AS tor_length_miles,
    CAST("TOR_WIDTH" AS DOUBLE)                                         AS tor_width_yards,
    "TOR_OTHER_WFO"                                                     AS tor_other_wfo,
    "TOR_OTHER_CZ_STATE"                                                AS tor_other_cz_state,
    CAST("TOR_OTHER_CZ_FIPS" AS INTEGER)                                AS tor_other_cz_fips,
    "TOR_OTHER_CZ_NAME"                                                 AS tor_other_cz_name,
    CAST("BEGIN_RANGE" AS DOUBLE)                                       AS begin_range_miles,
    "BEGIN_AZIMUTH"                                                     AS begin_azimuth,
    "BEGIN_LOCATION"                                                    AS begin_location,
    CAST("END_RANGE" AS DOUBLE)                                         AS end_range_miles,
    "END_AZIMUTH"                                                       AS end_azimuth,
    "END_LOCATION"                                                      AS end_location,
    CAST("BEGIN_LAT" AS DOUBLE)                                         AS begin_lat,
    CAST("BEGIN_LON" AS DOUBLE)                                         AS begin_lon,
    CAST("END_LAT" AS DOUBLE)                                           AS end_lat,
    CAST("END_LON" AS DOUBLE)                                           AS end_lon,
    "SOURCE"                                                            AS report_source,
    "DATA_SOURCE"                                                       AS data_source,
    "EPISODE_NARRATIVE"                                                 AS episode_narrative,
    "EVENT_NARRATIVE"                                                   AS event_narrative
FROM "noaa-storm-events"
