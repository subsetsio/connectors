-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    "Dimension" AS dimension,
    "Factor" AS factor,
    "Indicator" AS indicator,
    "Indicator_Name" AS indicator_name,
    CAST("Year" AS BIGINT) AS year,
    "Nivel_de_madurez_texto_EN" AS nivel_de_madurez_texto_en,
    "source_resource"
FROM "idb-2016-cybersecurity-report-data-set"
