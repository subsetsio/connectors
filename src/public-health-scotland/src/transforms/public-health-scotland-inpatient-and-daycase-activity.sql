-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    "Quarter" AS quarter,
    "QuarterQF" AS quarterqf,
    "HB" AS hb,
    "HBQF" AS hbqf,
    "Location" AS location,
    "LocationQF" AS locationqf,
    "AdmissionType" AS admissiontype,
    "AdmissionTypeQF" AS admissiontypeqf,
    CAST("Episodes" AS BIGINT) AS episodes,
    CAST("LengthOfEpisode" AS BIGINT) AS lengthofepisode,
    CAST("AverageLengthOfEpisode" AS DOUBLE) AS averagelengthofepisode,
    "AverageLengthOfEpisodeQF" AS averagelengthofepisodeqf,
    CAST("Stays" AS BIGINT) AS stays,
    CAST("LengthOfStay" AS BIGINT) AS lengthofstay,
    CAST("AverageLengthOfStay" AS DOUBLE) AS averagelengthofstay,
    "AverageLengthOfStayQF" AS averagelengthofstayqf,
    "Sex" AS sex,
    "Age" AS age,
    CAST("SIMD" AS BIGINT) AS simd,
    "SIMDQF" AS simdqf,
    "Specialty" AS specialty,
    "SpecialtyName" AS specialtyname,
    CAST("Spells" AS BIGINT) AS spells,
    CAST("LengthOfSpell" AS BIGINT) AS lengthofspell,
    CAST("AverageLengthOfSpell" AS DOUBLE) AS averagelengthofspell,
    "AverageLengthOfSpellQF" AS averagelengthofspellqf,
    "HBT" AS hbt,
    "HBR" AS hbr,
    CAST("CrossBoundaryFlag" AS BIGINT) AS crossboundaryflag,
    "loc_name",
    "dqNotesIP" AS dqnotesip,
    "dqNotesOP" AS dqnotesop,
    "dqNotesBeds" AS dqnotesbeds
FROM "public-health-scotland-inpatient-and-daycase-activity"
