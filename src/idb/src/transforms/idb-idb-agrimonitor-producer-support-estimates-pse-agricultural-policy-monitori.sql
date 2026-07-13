-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country_id",
    "country",
    "country_es",
    "parent1name",
    "parent1name_es",
    "parent2name",
    "parent2name_es",
    "parent3name",
    "parent3name_es",
    "parent4name",
    "parent4name_es",
    CAST("ind_id" AS BIGINT) AS ind_id,
    "description",
    "description_es",
    "code",
    CAST("comm_id" AS BIGINT) AS comm_id,
    CAST("category" AS BIGINT) AS category,
    "unit",
    CAST("year" AS BIGINT) AS year,
    CAST("value" AS DOUBLE) AS value,
    "commoditie",
    "commoditie_es",
    "unitusd",
    CAST("valueusd" AS DOUBLE) AS valueusd,
    CAST("graph_order" AS DOUBLE) AS graph_order,
    "tstat",
    "source_resource"
FROM "idb-idb-agrimonitor-producer-support-estimates-pse-agricultural-policy-monitori"
