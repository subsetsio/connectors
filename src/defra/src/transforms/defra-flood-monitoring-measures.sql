SELECT
    notation,
    station_reference,
    label,
    parameter,
    parameter_name,
    qualifier,
    unit,
    unit_name,
    TRY_CAST(period AS BIGINT) AS period_seconds,
    value_type,
    datum_type
FROM "defra-flood-monitoring-measures"
WHERE notation IS NOT NULL AND notation <> ''
