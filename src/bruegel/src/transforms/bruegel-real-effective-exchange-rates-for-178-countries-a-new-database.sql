-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Frequency mixes monthly and annual observations in one table, and period is a source period code rather than a date. Filter frequency first. Country_set is the size of the trade-partner basket the exchange-rate index was computed against; pick one basket and do not aggregate across them.
SELECT
    "period",
    "measure",
    "frequency",
    CAST("country_set" AS BIGINT) AS country_set,
    "country_code",
    "value"
FROM "bruegel-real-effective-exchange-rates-for-178-countries-a-new-database"
