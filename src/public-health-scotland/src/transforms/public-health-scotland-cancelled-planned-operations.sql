-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No compact row identity was verified from the raw profile; rows are published as source observations and may include multiple cuts, measures, or suppressions from separate CKAN resources.
SELECT
    "resource_id",
    "resource_name",
    CAST("Month" AS BIGINT) AS month,
    "Hospital" AS hospital,
    CAST("TotalOperations" AS BIGINT) AS totaloperations,
    "TotalOperationsQF" AS totaloperationsqf,
    CAST("TotalCancelled" AS BIGINT) AS totalcancelled,
    "TotalCancelledQF" AS totalcancelledqf,
    CAST("CancelledByPatientReason" AS BIGINT) AS cancelledbypatientreason,
    "CancelledByPatientReasonQF" AS cancelledbypatientreasonqf,
    CAST("ClinicalReason" AS BIGINT) AS clinicalreason,
    "ClinicalReasonQF" AS clinicalreasonqf,
    CAST("NonClinicalCapacityReason" AS BIGINT) AS nonclinicalcapacityreason,
    "NonClinicalCapacityReasonQF" AS nonclinicalcapacityreasonqf,
    CAST("OtherReason" AS BIGINT) AS otherreason,
    "OtherReasonQF" AS otherreasonqf,
    CAST("UnknownReason" AS BIGINT) AS unknownreason,
    "UnknownReasonQF" AS unknownreasonqf,
    "HBT" AS hbt,
    "Country" AS country
FROM "public-health-scotland-cancelled-planned-operations"
