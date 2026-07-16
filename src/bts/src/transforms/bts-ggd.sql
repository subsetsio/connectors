-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("YEAR" AS BIGINT) AS year,
    CAST("MONTH" AS BIGINT) AS month,
    CAST("QUARTER" AS BIGINT) AS quarter,
    CAST("AIRLINE_ID" AS BIGINT) AS airline_id,
    "CARRIER" AS carrier,
    "CARRIER_NAME" AS carrier_name,
    "UNIQUE_CARRIER" AS unique_carrier,
    "UNIQUE_CARRIER_NAME" AS unique_carrier_name,
    "PASSENGERS" AS passengers,
    CAST("MISHANDLED_BAGGAGE" AS BIGINT) AS mishandled_baggage,
    CAST("ENPLANED_BAGGAGE" AS BIGINT) AS enplaned_baggage,
    CAST("MISHANDLED_WCHR_SCTR" AS BIGINT) AS mishandled_wchr_sctr,
    CAST("ENPLANED_WCHR_SCTR" AS BIGINT) AS enplaned_wchr_sctr,
    "FORM_TYPE" AS form_type,
    "obs_date",
    "obs_year",
    "obs_period"
FROM "bts-ggd"
