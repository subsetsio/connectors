-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Indicator_number" AS indicator_number,
    "Project_number" AS project_number,
    "Project_name" AS project_name,
    "Country" AS country,
    "Entity" AS entity,
    CAST("Year" AS BIGINT) AS year,
    CAST("Progress" AS BIGINT) AS progress,
    "source_resource"
FROM "idb-idb-group-impact-framework-portfolio-results-dataset"
