-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Facility ID" AS facility_id,
    "Facility Name" AS facility_name,
    CAST("MSA" AS BIGINT) AS msa,
    "MSA Title" AS msa_title,
    "HCAHPS HLMR" AS hcahps_hlmr,
    "HCAHPS HLMR Percentile" AS hcahps_hlmr_percentile,
    "HCAHPS Start Date" AS hcahps_start_date,
    strptime("HCAHPS End Date", '%m/%d/%Y')::DATE AS hcahps_end_date,
    "HCAHPS Footnote" AS hcahps_footnote,
    "COMP-HIP-KNEE" AS comp_hip_knee,
    "COMP-HIP-KNEE Percentile" AS comp_hip_knee_percentile,
    "COMP Start Date" AS comp_start_date,
    strptime("COMP End Date", '%m/%d/%Y')::DATE AS comp_end_date,
    "COMP Footnote" AS comp_footnote,
    "PRO" AS pro,
    "PRO Start Date" AS pro_start_date,
    strptime("PRO End Date", '%m/%d/%Y')::DATE AS pro_end_date,
    "Reconciliation Footnote" AS reconciliation_footnote
FROM "cms-tqkv-mgxq"
