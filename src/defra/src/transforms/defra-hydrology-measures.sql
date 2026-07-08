SELECT
    notation,
    station,
    label,
    parameter,
    parameter_name,
    observed_property,
    value_statistic,
    TRY_CAST(period AS BIGINT) AS period_seconds,
    period_name,
    unit,
    unit_name,
    observation_type
FROM "defra-hydrology-measures"
WHERE notation IS NOT NULL AND notation <> ''
