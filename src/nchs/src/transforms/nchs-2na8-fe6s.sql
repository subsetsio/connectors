-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
SELECT
    strptime("data_as_of", '%m/%d/%Y')::DATE AS data_as_of,
    "start_date",
    strptime("end_date", '%m/%d/%Y')::DATE AS end_date,
    "country",
    "year",
    "month",
    "sex",
    "age_group",
    "race_and_hispanic_origin",
    "malignant_neoplasms_c00_c97",
    "malignant_neoplasms_of_lip_oral_cavity_and_pharynx_c00_c14",
    "malignant_neoplasm_of_esophagus_c15",
    "malignant_neoplasm_of_stomach_c16",
    "malignant_neoplasms_of_colon_rectum_and_anus_c18_c21",
    "malignant_neoplasms_of_liver_and_intrahepatic_bile_ducts_c22",
    "malignant_neoplasm_of_pancreas_c25",
    "malignant_neoplasm_of_larynx_c32",
    "malignant_neoplasms_of_trachea_bronchus_and_lung_c33_c34",
    "malignant_melanoma_of_skin_c43",
    "malignant_neoplasm_of_breast_c50",
    "malignant_neoplasm_of_cervix_uteri_c53",
    "corpus_uteri_cancer_c54_c55",
    "malignant_neoplasm_of_ovary_c56",
    "malignant_neoplasm_of_prostate_c61",
    "malignant_neoplasms_of_kidney_and_renal_pelvis_c64_c65",
    "malignant_neoplasm_of_bladder_c67",
    "cns_cancer_c70_c72",
    "lymphoid_hematopoietic_cancer_c81_c96",
    "other_unspecified_cancers_c17_c97"
FROM "nchs-2na8-fe6s"
