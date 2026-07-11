-- NIH RePORTER ExPORTER CLINICALSTUDY: ClinicalTrials.gov studies linked to NIH
-- projects. One row per (CORE_PROJECT_NUMBER, CLINICALTRIALS_GOV_ID) association
-- — a study may be supported by more than one project. Raw is stringly-typed
-- NDJSON from a single all-years file. No temporal axis (the export carries no
-- study start/completion date).
SELECT
    CORE_PROJECT_NUMBER   AS core_project_number,
    CLINICALTRIALS_GOV_ID AS clinicaltrials_gov_id,
    STUDY                 AS study,
    STUDY_STATUS          AS study_status
FROM "nih-clinicalstudy"
WHERE CORE_PROJECT_NUMBER IS NOT NULL
  AND CLINICALTRIALS_GOV_ID IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY CORE_PROJECT_NUMBER, CLINICALTRIALS_GOV_ID
    ORDER BY STUDY_STATUS DESC NULLS LAST
) = 1
