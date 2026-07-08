SELECT
    try_strptime(month, '%b-%Y')::DATE AS month,
    TRY_CAST(small_hydro_power AS DOUBLE) AS small_hydro_mw,
    TRY_CAST(wind_power AS DOUBLE)        AS wind_mw,
    TRY_CAST(bmpower_congen AS DOUBLE)    AS biomass_cogen_mw,
    TRY_CAST(wastetoenergy AS DOUBLE)     AS waste_to_energy_mw,
    TRY_CAST(solar_power AS DOUBLE)       AS solar_mw
FROM "cea-india-instcap-allindia-res"
WHERE month IS NOT NULL AND month <> ''
