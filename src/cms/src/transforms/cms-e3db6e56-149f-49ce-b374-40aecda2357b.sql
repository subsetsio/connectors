-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw profile; treat rows as source snapshot records, not entity-deduplicated facts.
SELECT
    "HCPCS_Cd" AS hcpcs_cd,
    "RBCS_Id" AS rbcs_id,
    "RBCS_Cat" AS rbcs_cat,
    "RBCS_Cat_Desc" AS rbcs_cat_desc,
    "RBCS_Cat_Subcat" AS rbcs_cat_subcat,
    "RBCS_Subcat_Desc" AS rbcs_subcat_desc,
    "RBCS_FamNumb" AS rbcs_famnumb,
    "RBCS_Family_Desc" AS rbcs_family_desc,
    "RBCS_Major_Ind" AS rbcs_major_ind,
    strptime("HCPCS_Cd_Add_Dt", '%m/%d/%Y')::DATE AS hcpcs_cd_add_dt,
    strptime("HCPCS_Cd_End_Dt", '%m/%d/%Y')::DATE AS hcpcs_cd_end_dt,
    CAST("RBCS_Latest_Assignment" AS BIGINT) AS rbcs_latest_assignment,
    CAST("First_RBCS_Release_Year" AS BIGINT) AS first_rbcs_release_year,
    strptime("RBCS_Analysis_Start_Dt", '%m/%d/%Y')::DATE AS rbcs_analysis_start_dt,
    strptime("RBCS_Analysis_End_Dt", '%m/%d/%Y')::DATE AS rbcs_analysis_end_dt,
    CAST("Alt_Assignment_Method" AS BIGINT) AS alt_assignment_method,
    CAST("RBCS_Id_Ever_Reassigned" AS BIGINT) AS rbcs_id_ever_reassigned
FROM "cms-e3db6e56-149f-49ce-b374-40aecda2357b"
