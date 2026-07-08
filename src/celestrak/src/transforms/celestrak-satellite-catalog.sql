SELECT
    norad_cat_id AS norad_id,
    object_id,
    object_name AS name,
    CASE object_type
        WHEN 'PAY' THEN 'PAYLOAD'
        WHEN 'R/B' THEN 'ROCKET_BODY'
        WHEN 'DEB' THEN 'DEBRIS'
        ELSE 'UNKNOWN'
    END AS object_type,
    CASE ops_status_code
        WHEN '+' THEN 'ACTIVE'
        WHEN '-' THEN 'INACTIVE'
        WHEN 'P' THEN 'PARTIALLY_OPERATIONAL'
        WHEN 'B' THEN 'BACKUP'
        WHEN 'S' THEN 'STANDBY'
        WHEN 'X' THEN 'EXTENDED'
        WHEN 'D' THEN 'DECAYED'
        ELSE 'UNKNOWN'
    END AS status,
    owner,
    launch_date,
    launch_site,
    decay_date,
    period AS period_minutes,
    inclination AS inclination_degrees,
    apogee AS apogee_km,
    perigee AS perigee_km
FROM "celestrak-satellite-catalog"
WHERE norad_cat_id IS NOT NULL
