-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    CAST("NPI" AS BIGINT) AS npi,
    "LAST_NAME" AS last_name,
    "FIRST_NAME" AS first_name,
    "PARTB" AS partb,
    "DME" AS dme,
    "HHA" AS hha,
    "PMD" AS pmd,
    "HOSPICE" AS hospice
FROM "cms-c99b5865-1119-4436-bb80-c5af2773ea1f"
