-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_database_id",
    "country_code",
    "indicator_code",
    "subindicator",
    CAST("inicial_year" AS BIGINT) AS inicial_year,
    CAST("year" AS BIGINT) AS year,
    CAST("aggregated_value" AS DOUBLE) AS aggregated_value,
    "aggregation_levenl",
    "uom",
    CAST("number" AS BIGINT) AS number,
    "question",
    "explicacion",
    "verificables",
    "idioma",
    "linka",
    "linkb",
    "linkc",
    "linkd",
    "source_resource"
FROM "idb-dataset-of-suburban-passenger-railways-in-latin-america-2018"
