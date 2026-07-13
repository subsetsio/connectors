SELECT
    make_date(year, month, 1)          AS date,
    NULLIF(sn_total, -1)               AS sn_total,
    NULLIF(sn_north, -1)               AS sn_north,
    NULLIF(sn_south, -1)               AS sn_south,
    NULLIF(std_total, -1)              AS std_total,
    NULLIF(std_north, -1)              AS std_north,
    NULLIF(std_south, -1)              AS std_south,
    NULLIF(n_obs_total, -1)            AS n_obs_total,
    NULLIF(n_obs_north, -1)            AS n_obs_north,
    NULLIF(n_obs_south, -1)            AS n_obs_south,
    definitive = 1                     AS definitive
FROM "silso-monthly-hemispheric"
