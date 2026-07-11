-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("PaidDateMonth" AS BIGINT) AS paiddatemonth,
    "PrescriberLocation" AS prescriberlocation,
    "PrescriberLocationPostcode" AS prescriberlocationpostcode,
    "PrescriberLocationType" AS prescriberlocationtype,
    "PrescriberType" AS prescribertype,
    CAST("DispenserLocation" AS BIGINT) AS dispenserlocation,
    "DispenserLocationPostcode" AS dispenserlocationpostcode,
    "DispenserLocationType" AS dispenserlocationtype,
    CAST("NumberOfPaidItems" AS BIGINT) AS numberofpaiditems
FROM "public-health-scotland-prescribed-dispensed"
