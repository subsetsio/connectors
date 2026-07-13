-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pais",
    CAST("gdpproj" AS BIGINT) AS gdpproj,
    CAST("infproj" AS BIGINT) AS infproj,
    CAST("spendproj" AS BIGINT) AS spendproj,
    CAST("revproj" AS BIGINT) AS revproj,
    CAST("expadmuproj" AS BIGINT) AS expadmuproj,
    CAST("expfunproj" AS BIGINT) AS expfunproj,
    CAST("disincproj" AS BIGINT) AS disincproj,
    CAST("expprogproj" AS BIGINT) AS expprogproj,
    CAST("resproj" AS BIGINT) AS resproj,
    CAST("mtff" AS BIGINT) AS mtff,
    CAST("mtbf" AS BIGINT) AS mtbf,
    CAST("mtef" AS BIGINT) AS mtef,
    CAST("mtbf_weak" AS BIGINT) AS mtbf_weak,
    CAST("mtef_weak" AS BIGINT) AS mtef_weak,
    CAST("urudum" AS BIGINT) AS urudum,
    "source_resource"
FROM "idb-medium-term-frameworks-and-the-budgetary-process-in-latin-america-a-databas"
