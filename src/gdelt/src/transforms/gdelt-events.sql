WITH rolled AS (
    SELECT
        CAST(date AS DATE) AS date,
        COALESCE(action_geo_country_iso2, 'XX') AS action_geo_country_iso2,
        event_root_code,
        CAST(quad_class AS TINYINT) AS quad_class,
        SUM(CAST(num_events AS BIGINT)) AS num_events,
        SUM(CAST(sum_mentions AS BIGINT)) AS sum_mentions,
        SUM(CAST(sum_articles AS BIGINT)) AS sum_articles,
        SUM(CAST(sum_goldstein AS DOUBLE)) AS tot_goldstein,
        SUM(CAST(sum_tone AS DOUBLE)) AS tot_tone
    FROM "gdelt-events"
    GROUP BY 1, 2, 3, 4
)
SELECT
    date,
    action_geo_country_iso2,
    event_root_code,
    CASE event_root_code
        WHEN '01' THEN 'Make Public Statement'
        WHEN '02' THEN 'Appeal'
        WHEN '03' THEN 'Express Intent to Cooperate'
        WHEN '04' THEN 'Consult'
        WHEN '05' THEN 'Engage in Diplomatic Cooperation'
        WHEN '06' THEN 'Engage in Material Cooperation'
        WHEN '07' THEN 'Provide Aid'
        WHEN '08' THEN 'Yield'
        WHEN '09' THEN 'Investigate'
        WHEN '10' THEN 'Demand'
        WHEN '11' THEN 'Disapprove'
        WHEN '12' THEN 'Reject'
        WHEN '13' THEN 'Threaten'
        WHEN '14' THEN 'Protest'
        WHEN '15' THEN 'Exhibit Force Posture'
        WHEN '16' THEN 'Reduce Relations'
        WHEN '17' THEN 'Coerce'
        WHEN '18' THEN 'Assault'
        WHEN '19' THEN 'Fight'
        WHEN '20' THEN 'Engage in Unconventional Mass Violence'
        ELSE NULL
    END AS event_root_label,
    quad_class,
    CASE quad_class
        WHEN 1 THEN 'Verbal Cooperation'
        WHEN 2 THEN 'Material Cooperation'
        WHEN 3 THEN 'Verbal Conflict'
        WHEN 4 THEN 'Material Conflict'
    END AS quad_class_label,
    num_events,
    sum_mentions,
    sum_articles,
    tot_goldstein / num_events AS avg_goldstein,
    tot_tone / num_events AS avg_tone
FROM rolled
WHERE num_events > 0
