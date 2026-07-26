-- temporary pass-through for an asset whose previous raw profile failed DuckDB JSON inference.
-- Regenerate with `hardened compile-transforms --write --force` after fresh raw profiles are measured.
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
    to_json("values") AS "values"
FROM "tokyo-metropolitan-government-statistics-t000003d2000001017"
