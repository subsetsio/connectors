-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("year" AS BIGINT) AS year,
    "isoalpha3",
    "iddate",
    "idgeo",
    "source",
    "indicator",
    "area",
    "quintile",
    "sex",
    "education_level",
    "age",
    "ethnicity",
    "disability",
    "migration",
    CAST("value" AS DOUBLE) AS value,
    CAST("level" AS BIGINT) AS level,
    CAST("se" AS DOUBLE) AS se,
    CAST("cv" AS DOUBLE) AS cv,
    CAST("sample" AS BIGINT) AS sample,
    CAST("quality_check" AS BIGINT) AS quality_check,
    "country",
    "pais",
    "area_es",
    "quintil_es",
    "etnicidad_es",
    "migracion_es",
    "discapacidad_es",
    "sex_es",
    "source_resource"
FROM "idb-olasscl-wash-household-survey-dataset"
