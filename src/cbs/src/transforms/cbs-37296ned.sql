-- Bevolking; kerncijfers (population key figures), annual, 1950 onward.
-- Grain: measure × period. No further dimensions in this table.
-- period_label is the bare year for this annual table → published as `year`.
-- string_value is 100% null here and value-less rows carry no observation,
-- so both are dropped.
SELECT
    "measure"                       AS measure,
    "measure_label"                 AS measure_label,
    "unit"                          AS unit,
    "period"                        AS period,
    CAST("period_label" AS BIGINT)  AS year,
    "value"                         AS value
FROM "cbs-37296ned"
WHERE "value" IS NOT NULL
