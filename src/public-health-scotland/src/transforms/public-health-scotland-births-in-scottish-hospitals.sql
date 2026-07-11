-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "FinancialYear" AS financialyear,
    "CA" AS ca,
    "Outcome" AS outcome,
    CAST("NRSBirths" AS BIGINT) AS nrsbirths,
    CAST("SMR02Births" AS BIGINT) AS smr02births,
    "Hospital" AS hospital,
    "SIMDQuintile" AS simdquintile,
    "SIMDQuintileQF" AS simdquintileqf,
    "SIMDVersion" AS simdversion,
    "AgeGroup" AS agegroup,
    "FirstBirth" AS firstbirth,
    "Maternities" AS maternities,
    "CAQF" AS caqf,
    "BookedBy12wks" AS bookedby12wks,
    "BMIGroup" AS bmigroup,
    "SmokingAtBooking" AS smokingatbooking,
    "AlcoholConsumption" AS alcoholconsumption,
    "MaternitiesQF" AS maternitiesqf,
    "HBR" AS hbr,
    "HBRQF" AS hbrqf,
    "FinancialYears" AS financialyears,
    "DrugMisuse" AS drugmisuse,
    "DrugMisuseQF" AS drugmisuseqf,
    "Delivery" AS delivery,
    "Induced" AS induced,
    CAST("Livebirths" AS BIGINT) AS livebirths,
    "Birthweight" AS birthweight,
    "Gestation" AS gestation,
    "BirthweightForGestationalAge" AS birthweightforgestationalage,
    "LevelOfCare" AS levelofcare,
    "BirthsAffectedByDrugs" AS birthsaffectedbydrugs,
    "BirthsAffectedByDrugsQF" AS birthsaffectedbydrugsqf
FROM "public-health-scotland-births-in-scottish-hospitals"
