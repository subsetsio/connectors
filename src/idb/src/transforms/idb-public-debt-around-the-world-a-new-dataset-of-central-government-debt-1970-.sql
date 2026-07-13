-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "wbcode",
    "country",
    CAST("year" AS BIGINT) AS year,
    CAST("DEBT_GDP" AS DOUBLE) AS debt_gdp,
    CAST("GDP" AS DOUBLE) AS gdp,
    "wbregion",
    CAST("incgroup" AS BIGINT) AS incgroup,
    CAST("balanced" AS BIGINT) AS balanced,
    CAST("group" AS BIGINT) AS group,
    "source_resource"
FROM "idb-public-debt-around-the-world-a-new-dataset-of-central-government-debt-1970-"
