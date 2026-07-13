-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Dimension" AS dimension,
    "Dimension_es" AS dimension_es,
    "Indicador" AS indicador,
    "Indicador_es" AS indicador_es,
    "Country" AS country,
    "Country_es" AS country_es,
    "Location" AS location,
    CAST("Year" AS BIGINT) AS year,
    "UOM" AS uom,
    CAST("Score" AS BIGINT) AS score,
    CAST("Normalized_Score_100" AS DOUBLE) AS normalized_score_100,
    "source_resource"
FROM "idb-2009-2014-infrascope-index-for-latin-america-and-the-caribbean"
