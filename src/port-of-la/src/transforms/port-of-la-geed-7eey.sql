SELECT
    harbor_tracking_no,
    film_la,
    filming_dates,
    TRY_CAST(harbor_fees AS DOUBLE) AS harbor_fees,
    location_s,
    production_co_title,
    comments
FROM "port-of-la-geed-7eey"
WHERE harbor_tracking_no IS NOT NULL
