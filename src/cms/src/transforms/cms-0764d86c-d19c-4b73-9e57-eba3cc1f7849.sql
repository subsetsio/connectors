-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Demonstration Project Name" AS demonstration_project_name,
    "Demonstration Type" AS demonstration_type,
    "Year" AS year,
    "Description" AS description,
    "URL" AS url,
    CAST("Unique ID" AS BIGINT) AS unique_id
FROM "cms-0764d86c-d19c-4b73-9e57-eba3cc1f7849"
