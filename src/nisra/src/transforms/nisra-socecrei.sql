-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistics" AS statistics,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census year" AS BIGINT) AS census_year,
    CAST("SOCEN" AS BIGINT) AS socen,
    "Socio-economic classification" AS socio_economic_classification,
    CAST("MEG" AS BIGINT) AS meg,
    "Ethnic group" AS ethnic_group,
    "UNIT" AS unit,
    "VALUE" AS value
FROM "nisra-socecrei"
