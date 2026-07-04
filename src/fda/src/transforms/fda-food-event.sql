-- fda-food-event: CAERS food (and dietary supplement/cosmetic legacy) adverse-event reports.
SELECT
    "report_number" AS report_number,
    CAST(try_strptime("date_created", '%Y%m%d') AS DATE) AS date_created,
    CAST(try_strptime("date_started", '%Y%m%d') AS DATE) AS date_started
FROM "fda-food-event"
