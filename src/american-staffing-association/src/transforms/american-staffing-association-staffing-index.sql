SELECT
    strptime(week_ending, '%-m/%-d/%Y')::DATE AS week_ending,
    CAST(staffing_index AS DOUBLE)            AS staffing_index,
    TRY_CAST(wow_change AS DOUBLE)            AS wow_change,
    TRY_CAST(four_week_average AS DOUBLE)     AS four_week_average
FROM "american-staffing-association-staffing-index"
WHERE week_ending IS NOT NULL
  AND staffing_index IS NOT NULL
