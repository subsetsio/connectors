-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "Reference_No" AS reference_no,
    "Project_Name" AS project_name,
    "Actual_Project_Name" AS actual_project_name,
    "Postal_Code" AS postal_code,
    "Rating" AS rating,
    "SLE_ZE_PE" AS sle_ze_pe,
    "CN" AS cn,
    "HW" AS hw,
    "IN" AS in,
    "MT" AS mt,
    "RE" AS re,
    "Prov_Letter" AS prov_letter,
    "e_cert",
    "Expiry" AS expiry,
    "Project_Type" AS project_type,
    "GFA" AS gfa,
    "Re_Certification" AS re_certification,
    "Previous_GM_Cert_Reference_No" AS previous_gm_cert_reference_no,
    "GM_Version" AS gm_version
FROM "sg-data-d-c4bd082b48fa7611713f39e23d250c27"
