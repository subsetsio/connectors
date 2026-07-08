SELECT variable, period,
       first_release, second_release, third_release, most_recent
FROM "philadelphia-fed-real-time-data-set-macroeconomists"
WHERE coalesce(first_release, second_release, third_release, most_recent) IS NOT NULL
ORDER BY variable, period
