SELECT
    CAST(id AS BIGINT)                      AS comet_id,
    type                                    AS comet_type,
    name,
    fullname,
    mpc_name,
    icq_name,
    component,
    TRY_CAST(current_mag AS DOUBLE)         AS current_mag,
    TRY_CAST(perihelion_date AS TIMESTAMP)  AS perihelion_date,
    TRY_CAST(perihelion_mag AS DOUBLE)      AS perihelion_mag,
    TRY_CAST(peak_mag AS DOUBLE)            AS peak_mag,
    TRY_CAST(peak_mag_date AS DATE)         AS peak_mag_date,
    CAST(is_observed AS BOOLEAN)            AS is_observed,
    CAST(is_active AS BOOLEAN)              AS is_active
FROM "cobs-comets"
WHERE id IS NOT NULL
