SELECT
    CAST(cm_mkey AS BIGINT)                       AS case_mkey,
    CAST(cm_ntsbNum AS VARCHAR)                   AS ntsb_number,
    CAST(cm_eventDate AS TIMESTAMP)               AS event_timestamp,
    CAST(cm_eventDate AS DATE)                    AS event_date,
    CAST(cm_eventType AS VARCHAR)                 AS event_type,
    CAST(cm_city AS VARCHAR)                      AS city,
    CAST(cm_state AS VARCHAR)                     AS state,
    CAST(cm_country AS VARCHAR)                   AS country,
    CAST(cm_Latitude AS DOUBLE)                   AS latitude,
    CAST(cm_Longitude AS DOUBLE)                  AS longitude,
    CAST(airportId AS VARCHAR)                    AS airport_id,
    CAST(airportName AS VARCHAR)                  AS airport_name,
    CAST(accidentSiteCondition AS VARCHAR)        AS site_condition,
    CAST(cm_highestInjury AS VARCHAR)             AS highest_injury,
    CAST(cm_injuryOnboardCount AS BIGINT)         AS injury_onboard_count,
    CAST(cm_fatalInjuryCount AS BIGINT)           AS fatal_injury_count,
    CAST(cm_seriousInjuryCount AS BIGINT)         AS serious_injury_count,
    CAST(cm_minorInjuryCount AS BIGINT)           AS minor_injury_count,
    CAST(cm_onboard_None AS BIGINT)               AS uninjured_count,
    CAST(cm_onboard_Total AS BIGINT)              AS onboard_total,
    CAST(cm_HazmatInvolved AS BOOLEAN)            AS hazmat_involved,
    CAST(cm_hasSafetyRec AS BOOLEAN)              AS has_safety_rec,
    CAST(cm_agency AS VARCHAR)                    AS agency,
    CAST(cm_launch AS VARCHAR)                    AS launch,
    CAST(cm_closed AS BOOLEAN)                    AS is_closed,
    CAST(cm_completionStatus AS VARCHAR)          AS completion_status,
    CAST(cm_mostRecentReportType AS VARCHAR)      AS most_recent_report_type,
    CAST(cm_recentReportPublishDate AS TIMESTAMP) AS recent_report_publish_date,
    CAST(cm_originalPublishedDate AS TIMESTAMP)   AS original_published_date
FROM "ntsb-aviation-accidents"
WHERE cm_mkey IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY cm_mkey
    ORDER BY cm_recentReportPublishDate DESC NULLS LAST
) = 1
