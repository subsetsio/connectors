-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Long-format observations spanning ~17,100 heterogeneous series (CPI, GDP, FX rates, interest rates, balance of payments, fiscal, expectations) in many different units — never aggregate value across codigo_serie; always filter to a single series (join central-bank-of-peru-series for its unit and label).
-- caution: frecuencia mixes Diaria/Mensual/Trimestral/Anual across rows, so the date column carries different granularities depending on the series — filter by frecuencia (or a single codigo_serie) before any time aggregation.
SELECT
    "codigo_serie",
    "frecuencia",
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "value"
FROM "central-bank-of-peru-values"
