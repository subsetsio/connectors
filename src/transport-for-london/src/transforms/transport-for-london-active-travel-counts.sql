-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are directional count observations by site, survey date, time interval, path, mode, and programme wave, but the raw source includes duplicate and blank-measurement rows; aggregate only after choosing the modes and directions relevant to the question.
SELECT
    "wave",
    "site_id",
    "date" AS source_date,
    CASE
        WHEN parsed_date > DATE '2026-01-01' AND wave_year IS NOT NULL
            THEN make_date(wave_year, date_part('month', parsed_date)::INTEGER, date_part('day', parsed_date)::INTEGER)
        ELSE parsed_date
    END AS date,
    parsed_date > DATE '2026-01-01' AND wave_year IS NOT NULL AS date_corrected_from_wave_year,
    "weather",
    "time",
    "day",
    "round",
    "direction",
    "path",
    "mode",
    CAST("count" AS BIGINT) AS count
FROM (
    SELECT
        *,
        strptime("date", '%d/%m/%Y')::DATE AS parsed_date,
        NULLIF(regexp_extract("wave", '^(\\d{4})', 1), '')::INTEGER AS wave_year
    FROM "transport-for-london-active-travel-counts"
)
