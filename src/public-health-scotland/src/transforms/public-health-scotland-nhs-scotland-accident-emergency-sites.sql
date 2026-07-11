-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "resource_id",
    "resource_name",
    "HB" AS hb,
    "TreatmentLocationName" AS treatmentlocationname,
    "TreatmentLocationCode" AS treatmentlocationcode,
    "TreatmentLocationPostcode" AS treatmentlocationpostcode,
    "CurrentDepartmentType" AS currentdepartmenttype,
    "FileType" AS filetype,
    "Comments" AS comments,
    "Status" AS status
FROM "public-health-scotland-nhs-scotland-accident-emergency-sites"
