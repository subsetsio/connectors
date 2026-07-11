-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Date" AS date,
    "KeyStatistic" AS keystatistic,
    "CA" AS ca,
    "MainClientGroup" AS mainclientgroup,
    "Sector" AS sector,
    "Unit" AS unit,
    "Value" AS value,
    "ValueQF" AS valueqf,
    "DateOrFinancialYear" AS dateorfinancialyear,
    "CAQF" AS caqf,
    "MainClientGroupQF" AS mainclientgroupqf,
    "SectorQF" AS sectorqf
FROM "public-health-scotland-care-home-census"
