-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    strptime("date", '%d/%m/%Y')::DATE AS date,
    strptime("date_predicted", '%d/%m/%Y')::DATE AS date_predicted,
    CAST("inflation_mean" AS DOUBLE) AS inflation_mean,
    CAST("growth_mean" AS DOUBLE) AS growth_mean,
    "source_resource"
FROM "idb-database-for-revelation-of-expectations-in-latin-america-revela"
