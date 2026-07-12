SELECT
    measure_name,
    measure,
    measure_subtype,
    market,
    factor,
    units,
    type,
    subtype,
    alternative_name,
    source_raw AS source
FROM "allen-unger-commodity-prices-measures"
WHERE measure_name IS NOT NULL
  AND measure IS NOT NULL
  AND market IS NOT NULL
