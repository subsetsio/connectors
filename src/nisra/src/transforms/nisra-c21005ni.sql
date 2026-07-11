-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "STATISTIC" AS statistic,
    "Statistic Label" AS statistic_label,
    CAST("TLIST(A1)" AS BIGINT) AS tlist_a1,
    CAST("Census Year" AS BIGINT) AS census_year,
    "NI" AS ni,
    "Northern Ireland" AS northern_ireland,
    CAST("ETHNIC_GROUP_INTERMEDIATE" AS BIGINT) AS ethnic_group_intermediate,
    "Ethnic group" AS ethnic_group,
    "UNIT" AS unit,
    CAST("VALUE" AS BIGINT) AS value
FROM "nisra-c21005ni"
