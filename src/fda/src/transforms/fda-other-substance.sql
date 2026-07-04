-- fda-other-substance: GSRS substance registration records (UNII registry).
SELECT
    "uuid" AS uuid,
    NULLIF(trim("unii"), '') AS unii,
    "substance_class" AS substance_class,
    "definition_type" AS definition_type,
    "definition_level" AS definition_level,
    TRY_CAST(TRY_CAST("version" AS DOUBLE) AS BIGINT) AS version
FROM "fda-other-substance"
