SELECT
    * EXCLUDE (lower_chamber_percent_women, upper_chamber_percent_women),
    TRY_CAST(lower_chamber_percent_women AS DOUBLE) AS lower_chamber_percent_women,
    TRY_CAST(upper_chamber_percent_women AS DOUBLE) AS upper_chamber_percent_women
FROM "inter-parliamentary-union-report-women-ranking"
WHERE "country_code" IS NOT NULL
