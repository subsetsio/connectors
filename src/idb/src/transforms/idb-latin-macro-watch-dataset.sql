-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("lmwuuid" AS BIGINT) AS lmwuuid,
    "Country" AS country,
    "Frequency" AS frequency,
    CAST("Year" AS BIGINT) AS year,
    strptime("Date", '%Y-%m-%d')::DATE AS date,
    CAST("Value" AS DOUBLE) AS value,
    "Indicator" AS indicator,
    "Unit" AS unit,
    "Transformation" AS transformation,
    "Area" AS area,
    "Topic" AS topic,
    "Definition" AS definition,
    "Source" AS source,
    "Notes" AS notes,
    strptime("Updated", '%Y-%m-%d')::DATE AS updated,
    "source_resource"
FROM "idb-latin-macro-watch-dataset"
