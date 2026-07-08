WITH ranked AS (
    SELECT *, row_number() OVER (
        PARTITION BY id
        ORDER BY TRY_CAST(lastUpdateDateTime AS TIMESTAMP) DESC NULLS LAST
    ) AS rn
    FROM "entsog-transparency-platform-cmpunsuccessfulrequests"
)
SELECT
    id,
    operatorKey                                     AS operator_key,
    operatorLabel                                   AS operator_label,
    pointKey                                        AS point_key,
    pointLabel                                      AS point_label,
    directionKey                                    AS direction_key,
    TRY_CAST(NULLIF(requestedVolume, '') AS DOUBLE)   AS requested_volume,
    TRY_CAST(NULLIF(allocatedVolume, '') AS DOUBLE)   AS allocated_volume,
    TRY_CAST(NULLIF(unallocatedVolume, '') AS DOUBLE) AS unallocated_volume,
    TRY_CAST(NULLIF(occurenceCount, '') AS BIGINT)    AS occurence_count,
    NULLIF(generalRemarks, '')                      AS general_remarks,
    TRY_CAST(lastUpdateDateTime AS TIMESTAMP)         AS last_update
FROM ranked
WHERE rn = 1
