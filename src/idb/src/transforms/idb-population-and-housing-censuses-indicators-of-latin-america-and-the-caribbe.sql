-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iddate",
    CAST("year" AS BIGINT) AS year,
    "idgeo",
    "isoalpha3",
    "source",
    "indicator",
    "area",
    "quintile",
    "sex",
    "education_level",
    "age",
    "ethnicity",
    CAST("value" AS DOUBLE) AS value,
    CAST("se" AS DOUBLE) AS se,
    CAST("cv" AS DOUBLE) AS cv,
    CAST("sample" AS BIGINT) AS sample,
    "source_resource"
FROM "idb-population-and-housing-censuses-indicators-of-latin-america-and-the-caribbe"
