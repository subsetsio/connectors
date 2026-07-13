-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "COUNTRY" AS country,
    "PAIS" AS pais,
    "GRUPO" AS grupo,
    "INDICATOR" AS indicator,
    "INDICADOR" AS indicador,
    CAST("INDICATOR_ID" AS BIGINT) AS indicator_id,
    "Sub-Indicator_If_Applicable" AS sub_indicator_if_applicable,
    CAST("Sub-Indicator_ID_If_Applicable" AS DOUBLE) AS sub_indicator_id_if_applicable,
    "LEVEL" AS level,
    "LEVEL_NAME" AS level_name,
    CAST("VALUE" AS BIGINT) AS value,
    "UNIT" AS unit,
    "COMPLEMENTARY_DATA" AS complementary_data,
    CAST("Year_Date" AS BIGINT) AS year_date,
    CAST("Year_Text" AS BIGINT) AS year_text,
    "NOTES" AS notes,
    "NOTAS" AS notas,
    "SOURCE" AS source,
    "source_resource"
FROM "idb-dataset-of-housing-indicators-in-argentina-brazil-colombia-and-mexico-2000-"
