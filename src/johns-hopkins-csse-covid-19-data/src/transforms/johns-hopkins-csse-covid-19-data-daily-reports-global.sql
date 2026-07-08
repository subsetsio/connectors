SELECT
    CAST(report_date AS DATE)                   AS date,
    fips,
    admin2,
    province_state,
    country_region,
    combined_key,
    TRY_CAST(lat AS DOUBLE)                     AS lat,
    TRY_CAST(long AS DOUBLE)                    AS long,
    TRY_CAST(TRY_CAST(confirmed AS DOUBLE) AS BIGINT) AS confirmed,
    TRY_CAST(TRY_CAST(deaths AS DOUBLE) AS BIGINT)    AS deaths,
    TRY_CAST(TRY_CAST(recovered AS DOUBLE) AS BIGINT) AS recovered,
    TRY_CAST(TRY_CAST(active AS DOUBLE) AS BIGINT)    AS active,
    TRY_CAST(incident_rate AS DOUBLE)          AS incident_rate,
    TRY_CAST(case_fatality_ratio AS DOUBLE)    AS case_fatality_ratio
FROM "johns-hopkins-csse-covid-19-data-daily-reports-global"
