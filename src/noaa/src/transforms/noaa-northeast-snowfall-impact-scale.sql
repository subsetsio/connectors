-- Rank carries a trailing 0xFF byte in the upstream CSV ("1\xff"); strip the
-- non-digits before casting. Dates are m/d/Y with unpadded fields.
SELECT
    CAST(regexp_replace("Rank", '[^0-9]', '', 'g') AS INTEGER)  AS "rank",
    strptime("Start Date", '%m/%d/%Y')::DATE                    AS start_date,
    strptime("End Dat", '%m/%d/%Y')::DATE                       AS end_date,
    CAST("NESIS" AS DOUBLE)                                     AS nesis,
    CAST("Category" AS INTEGER)                                 AS category,
    "Description"                                               AS category_label
FROM "noaa-northeast-snowfall-impact-scale"
