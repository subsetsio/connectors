-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("area_type" AS BIGINT) AS area_type,
    CAST("area" AS BIGINT) AS area,
    "area_name",
    "standard_occupational_code",
    "occupational_title",
    CAST("employment" AS BIGINT) AS employment,
    CAST("mean" AS DOUBLE) AS mean,
    CAST("median" AS DOUBLE) AS median,
    CAST("entry_wage" AS DOUBLE) AS entry_wage,
    CAST("experienced_wage" AS DOUBLE) AS experienced_wage
FROM "new-york-state-department-of-labor-gkgz-nw24"
