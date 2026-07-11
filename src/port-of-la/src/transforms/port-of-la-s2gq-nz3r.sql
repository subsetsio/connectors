SELECT
    harbor_department,
    TRY_CAST(jul AS DOUBLE) AS jul,
    TRY_CAST(aug AS DOUBLE) AS aug,
    TRY_CAST(sept AS DOUBLE) AS sept,
    TRY_CAST(oct AS DOUBLE) AS oct,
    TRY_CAST(nov AS DOUBLE) AS nov,
    TRY_CAST(dec AS DOUBLE) AS dec,
    TRY_CAST(jan AS DOUBLE) AS jan,
    TRY_CAST(feb AS DOUBLE) AS feb,
    TRY_CAST(mar AS DOUBLE) AS mar,
    TRY_CAST(apr AS DOUBLE) AS apr,
    TRY_CAST(may AS DOUBLE) AS may,
    TRY_CAST(jun AS DOUBLE) AS jun,
    TRY_CAST(total AS DOUBLE) AS total,
    TRY_CAST(adjustment AS DOUBLE) AS adjustment,
    TRY_CAST(net_total AS DOUBLE) AS net_total
FROM "port-of-la-s2gq-nz3r"
WHERE harbor_department IS NOT NULL
