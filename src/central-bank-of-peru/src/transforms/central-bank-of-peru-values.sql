-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns), then curated: Spanish source columns
-- renamed to snake_case English; casts unchanged from the compile.
-- caution: Long-format observations spanning ~17,100 heterogeneous series (CPI, GDP, FX rates, interest rates, balance of payments, fiscal, expectations) in many different units — never aggregate value across series_code; always filter to a single series (join central-bank-of-peru-series for its unit and label).
-- caution: frequency mixes Diaria/Mensual/Trimestral/Anual across rows, so the date column carries different granularities depending on the series — filter by frequency (or a single series_code) before any time aggregation.
SELECT
    "codigo_serie"                 AS series_code,
    "frecuencia"                   AS frequency,
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value"                        AS value
FROM "central-bank-of-peru-values"
