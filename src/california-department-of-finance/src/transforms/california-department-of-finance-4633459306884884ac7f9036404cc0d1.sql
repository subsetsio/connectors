-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "County" AS county,
    "SubCounty" AS subcounty,
    "Sub" AS sub,
    "Jurisdiction" AS jurisdiction,
    "textJurisdiction" AS textjurisdiction,
    "name",
    "Sort" AS sort,
    "FID" AS fid,
    "bannername"
FROM "california-department-of-finance-4633459306884884ac7f9036404cc0d1"
