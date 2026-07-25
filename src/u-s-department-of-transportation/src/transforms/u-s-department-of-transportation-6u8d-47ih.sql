-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("quarter" AS BIGINT) AS quarter,
    CAST("airline_id" AS BIGINT) AS airline_id,
    "carrier",
    "carrier_name",
    "unique_carrier",
    "unique_carrier_name",
    CAST("passengers" AS BIGINT) AS passengers,
    CAST("mishandled_baggage" AS BIGINT) AS mishandled_baggage,
    CAST("enplaned_baggage" AS BIGINT) AS enplaned_baggage,
    CAST("mishandled_wchr_sctr" AS BIGINT) AS mishandled_wchr_sctr,
    CAST("enplaned_wchr_sctr" AS BIGINT) AS enplaned_wchr_sctr,
    "form_type",
    CAST("mkt_carrier_flag" AS BOOLEAN) AS mkt_carrier_flag
FROM "u-s-department-of-transportation-6u8d-47ih"
