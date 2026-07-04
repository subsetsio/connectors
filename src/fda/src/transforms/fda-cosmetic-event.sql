-- fda-cosmetic-event: MoCRA/CAERS cosmetic adverse-event reports. Dropped: meddra_version (constant) and event_date (Excel-mangled free text like '01-Apr').
SELECT
    TRY_CAST(TRY_CAST("report_number" AS DOUBLE) AS BIGINT) AS report_number,
    "report_type" AS report_type,
    TRY_CAST(TRY_CAST("report_version" AS DOUBLE) AS INTEGER) AS report_version,
    NULLIF(trim("legacy_report_id"), '') AS legacy_report_id,
    CAST(try_strptime("initial_received_date", '%Y%m%d') AS DATE) AS initial_received_date,
    CAST(try_strptime("latest_received_date", '%Y%m%d') AS DATE) AS latest_received_date
FROM "fda-cosmetic-event"
