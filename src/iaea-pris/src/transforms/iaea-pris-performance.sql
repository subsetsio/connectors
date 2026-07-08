SELECT
    reactor_id,
    year,
    electricity_supplied_gwh,
    reference_unit_power_mw,
    annual_time_on_line_h,
    operation_factor_pct,
    energy_availability_factor_pct,
    load_factor_pct
FROM "iaea-pris-performance"
WHERE electricity_supplied_gwh IS NOT NULL
   OR annual_time_on_line_h IS NOT NULL
   OR load_factor_pct IS NOT NULL
