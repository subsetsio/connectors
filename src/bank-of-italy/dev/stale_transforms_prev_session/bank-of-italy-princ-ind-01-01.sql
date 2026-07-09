WITH src AS (SELECT to_json(d) AS j FROM "bank-of-italy-princ-ind-01-01" d)
SELECT date, series_key, value FROM (
    SELECT
        TRY_CAST(COALESCE(j->>'DATA_OSS', j->>'DATA_DECOR', j->>'DATA_PROV') AS TIMESTAMP)::DATE AS date,
        concat_ws(':', j->>'CUBEID', j->>'MEASURES') AS series_key,
        TRY_CAST(j ->> (j->>'MEASURES') AS DOUBLE) AS value,
        j->>'DATA_PROV' AS _prov,
        TRY_CAST(j->>'NUM_ORD' AS BIGINT) AS _ord
    FROM src
)
WHERE date IS NOT NULL AND value IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY date, series_key ORDER BY _prov DESC NULLS LAST, _ord DESC NULLS LAST
) = 1
