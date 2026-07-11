-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "HBT" AS hbt,
    CAST("DispLocationCode" AS BIGINT) AS displocationcode,
    "DMDCode" AS dmdcode,
    "BNFItemCode" AS bnfitemcode,
    "BNFItemDescription" AS bnfitemdescription,
    "PrescribedType" AS prescribedtype,
    CAST("NumberOfPaidItems" AS BIGINT) AS numberofpaiditems,
    CAST("PaidQuantity" AS BIGINT) AS paidquantity,
    CAST("GrossIngredientCost" AS DOUBLE) AS grossingredientcost,
    CAST("PaidDateMonth" AS BIGINT) AS paiddatemonth,
    CAST("GPPractice" AS BIGINT) AS gppractice,
    "ClassOfPreparationCode" AS classofpreparationcode,
    "HBT2014" AS hbt2014
FROM "public-health-scotland-prescriptions-in-the-community"
