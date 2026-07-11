-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HB" AS hb,
    "SMRType" AS smrtype,
    "Quarter" AS quarter,
    CAST("Completeness" AS DOUBLE) AS completeness,
    "CompletenessQF" AS completenessqf,
    "FinancialYear" AS financialyear,
    CAST("CalendarYear" AS BIGINT) AS calendaryear
FROM "public-health-scotland-scottish-morbidity-record-completeness"
