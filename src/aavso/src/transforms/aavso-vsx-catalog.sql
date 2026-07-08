SELECT
    recno,
    OID                                   AS oid,
    TRIM(Name)                            AS name,
    V                                     AS variability_flag,
    RAJ2000                               AS ra_deg,
    DEJ2000                               AS dec_deg,
    NULLIF(TRIM(Type), '')                AS variability_type,
    NULLIF(TRIM(l_max), '')               AS max_mag_limit_flag,
    "max"                                 AS max_mag,
    NULLIF(TRIM(n_max), '')               AS max_mag_band,
    NULLIF(TRIM(f_min), '')               AS min_is_amplitude_flag,
    NULLIF(TRIM(l_min), '')               AS min_mag_limit_flag,
    "min"                                 AS min_mag,
    NULLIF(TRIM(n_min), '')               AS min_mag_band,
    Epoch                                 AS epoch_jd,
    Period                                AS period_days,
    NULLIF(TRIM(Sp), '')                  AS spectral_type
FROM "aavso-vsx-catalog"
WHERE OID IS NOT NULL
