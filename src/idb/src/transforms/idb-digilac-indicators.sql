-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator" AS indicator,
    "Country" AS country,
    CAST("Year" AS BIGINT) AS year,
    CAST("Value_Real" AS DOUBLE) AS value_real,
    CAST("Value_Normalized" AS DOUBLE) AS value_normalized,
    "source_resource"
FROM "idb-digilac-indicators"
