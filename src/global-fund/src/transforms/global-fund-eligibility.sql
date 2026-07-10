-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Eligibility rows are country/component/year observations; filter component and allocation period before counting eligible countries.
SELECT
    "eligibilityId" AS eligibilityid,
    "geographyId" AS geographyid,
    "incomeLevel" AS incomelevel,
    "activityAreaId" AS activityareaid,
    "diseaseBurden" AS diseaseburden,
    "isEligible" AS iseligible,
    "eligibilityYear" AS eligibilityyear,
    "fundingStream" AS fundingstream,
    "policyReference" AS policyreference,
    "notes",
    "dateTimeCreated" AS datetimecreated,
    "dateTimeUpdated" AS datetimeupdated
FROM "global-fund-eligibility"
