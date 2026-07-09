-- India's official foreign exchange reserves, long format, one row per
-- (observation_date, reserve_code, frequency).
--
-- Residuals over the compiled pass-through:
--   * observation_date is an ISO string in raw -> DATE
--   * reserve_name carries the RBI's printed row numbering ("1.1 Foreign
--     Currency Assets") -> stripped to a plain label
--   * currency_code / unit / unit_description are constant ('USD', 1,
--     'ACTUALS') -> dropped, folded into the amount description
--   * timedate_ms is the epoch-millis observation_date was derived from -> dropped
--   * a null amount marks a date where the component was not yet reported
--     (early SDR / IMF history) -> no observation, dropped
--
-- caution: Weekly and Monthly observations share this date column and overlap
-- on month-end reporting Fridays — filter `frequency` before aggregating.
-- caution: reserve_code 'TR' is the sum of FCA + GOLD + SDR + IMF for the same
-- date and frequency — exclude it before summing across components.
SELECT
    strptime(observation_date, '%Y-%m-%d')::DATE AS observation_date,
    CAST(reserve_code AS VARCHAR) AS reserve_code,
    regexp_replace(reserve_name, '^[0-9.]+\s+', '') AS reserve_name,
    CAST(frequency AS VARCHAR) AS frequency,
    CAST(amount AS DOUBLE) AS amount,
    CAST(fiscal_year AS VARCHAR) AS fiscal_year
FROM "rbi-foreign-exchange-reserves"
WHERE observation_date IS NOT NULL
  AND amount IS NOT NULL
