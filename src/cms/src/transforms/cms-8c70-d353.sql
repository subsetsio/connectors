-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility Name" AS facility_name,
    "org_PAC_ID" AS org_pac_id,
    "measure_cd",
    "measure_title",
    "prf_rate",
    "patient_count",
    "FN" AS fn
FROM "cms-8c70-d353"
