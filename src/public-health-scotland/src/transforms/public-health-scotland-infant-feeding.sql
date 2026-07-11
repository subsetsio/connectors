-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Review" AS review,
    "FinancialYear" AS financialyear,
    "HBR" AS hbr,
    "CA" AS ca,
    "MotherAgeGroup" AS motheragegroup,
    CAST("ValidReviews" AS BIGINT) AS validreviews,
    CAST("CurrentFeedingExclusiveBreast" AS BIGINT) AS currentfeedingexclusivebreast,
    CAST("CurrentFeedingMixed" AS BIGINT) AS currentfeedingmixed,
    CAST("CurrentFeedingFormula" AS BIGINT) AS currentfeedingformula,
    CAST("CurrentFeedingOther" AS BIGINT) AS currentfeedingother,
    CAST("CurrentFeedingCowsMilk" AS BIGINT) AS currentfeedingcowsmilk,
    CAST("CurrentFeedingOverallBreast" AS BIGINT) AS currentfeedingoverallbreast,
    CAST("EverBreastfed" AS BIGINT) AS everbreastfed,
    CAST("ExclusivelyBreastfedSinceBirth" AS BIGINT) AS exclusivelybreastfedsincebirth,
    "SIMDQuintile" AS simdquintile,
    "SIMDQuintileQF" AS simdquintileqf,
    "SIMDVersion" AS simdversion,
    "MaternalSmoking" AS maternalsmoking,
    CAST("Age5Weeks" AS BIGINT) AS age5weeks,
    CAST("Age6Weeks" AS BIGINT) AS age6weeks,
    CAST("Age7Weeks" AS BIGINT) AS age7weeks,
    CAST("Age8Weeks" AS BIGINT) AS age8weeks,
    CAST("Age9Weeks" AS BIGINT) AS age9weeks,
    CAST("Age10Weeks" AS BIGINT) AS age10weeks,
    CAST("Age11Weeks" AS BIGINT) AS age11weeks,
    CAST("Age12Weeks" AS BIGINT) AS age12weeks,
    CAST("OtherAge" AS BIGINT) AS otherage,
    CAST("TotalReviews" AS BIGINT) AS totalreviews,
    CAST("ChildrenEligibleForReview" AS BIGINT) AS childreneligibleforreview
FROM "public-health-scotland-infant-feeding"
