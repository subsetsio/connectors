-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    CAST("Year" AS BIGINT) AS year,
    "Indicator" AS indicator,
    "Note" AS note,
    "Source" AS source,
    CAST("Value" AS DOUBLE) AS value,
    "source_resource"
FROM "idb-summary-indicators-of-employment-protection-legislation-epl-in-latin-americ"
