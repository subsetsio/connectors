-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "GeographyType" AS geographytype,
    "Geography" AS geography,
    "GeographyQF" AS geographyqf,
    "UserType" AS usertype,
    "UserTypeQF" AS usertypeqf,
    "Sex" AS sex,
    "SexQF" AS sexqf,
    "AgeGroup" AS agegroup,
    "AgeGroupQF" AS agegroupqf,
    CAST("NumberStartingTreatment" AS BIGINT) AS numberstartingtreatment,
    "NumberStartingTreatmentQF" AS numberstartingtreatmentqf,
    CAST("PercentageStartingTreatment" AS DOUBLE) AS percentagestartingtreatment,
    "PercentageStartingTreatmentQF" AS percentagestartingtreatmentqf,
    CAST("Total" AS BIGINT) AS total,
    "TotalQF" AS totalqf
FROM "public-health-scotland-initial-assessments-for-specialist-drug-and-alcohol-treatment"
