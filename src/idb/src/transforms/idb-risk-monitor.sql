-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_database_id",
    "country_code",
    "indicator_code",
    "subindicator",
    CAST("inicial_year" AS DOUBLE) AS inicial_year,
    CAST("year" AS DOUBLE) AS year,
    CAST("aggregated_value" AS DOUBLE) AS aggregated_value,
    "aggregation_levenl",
    "uom",
    CAST("number" AS DOUBLE) AS number,
    "question",
    "explicacion",
    "verificables",
    "idioma",
    "linka",
    "linkb",
    "linkc",
    "linkd",
    "source_resource"
FROM "idb-risk-monitor"
