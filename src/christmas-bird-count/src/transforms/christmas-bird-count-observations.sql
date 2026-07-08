SELECT
    circle_id,
    common_name,
    scientific_name,
    count_year,
    season_year,
    TRY_STRPTIME(count_date, '%m/%d/%Y')::DATE AS count_date,
    how_many,
    count_week_only,
    number_per_party_hours,
    flags
FROM "christmas-bird-count-observations"
WHERE common_name IS NOT NULL
  AND count_year IS NOT NULL
