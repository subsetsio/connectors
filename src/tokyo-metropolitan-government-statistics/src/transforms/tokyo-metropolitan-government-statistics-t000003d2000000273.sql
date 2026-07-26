-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table preserves the source package rows from one or more package resources; use the package and resource metadata columns to distinguish files or API endpoints before aggregating.
SELECT
    "entity_id",
    "package_id",
    "package_name",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_position",
    "resource_url_basename",
    "row_number",
    "values"
FROM "tokyo-metropolitan-government-statistics-t000003d2000000273"
