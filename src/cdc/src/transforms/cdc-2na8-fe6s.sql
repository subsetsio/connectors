-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("Data As Of", '%m/%d/%Y')::DATE AS data_as_of,
    "Start Date" AS start_date,
    strptime("End Date", '%m/%d/%Y')::DATE AS end_date,
    "Country" AS country,
    CAST("Year" AS BIGINT) AS year,
    CAST("Month" AS BIGINT) AS month,
    "Sex" AS sex,
    "Age Group" AS age_group,
    "Race and Hispanic Origin" AS race_and_hispanic_origin,
    CAST("Malignant neoplasms (C00-C97)" AS BIGINT) AS malignant_neoplasms_c00_c97,
    CAST("Malignant neoplasms of lip, oral cavity and pharynx (C00-C14)" AS BIGINT) AS malignant_neoplasms_of_lip_oral_cavity_and_pharynx_c00_c14,
    CAST("Malignant neoplasm of esophagus (C15)" AS BIGINT) AS malignant_neoplasm_of_esophagus_c15,
    CAST("Malignant neoplasm of stomach (C16)" AS BIGINT) AS malignant_neoplasm_of_stomach_c16,
    CAST("Malignant neoplasms of colon, rectum and anus (C18-C21)" AS BIGINT) AS malignant_neoplasms_of_colon_rectum_and_anus_c18_c21,
    CAST("Malignant neoplasms of liver and intrahepatic bile ducts (C22)" AS BIGINT) AS malignant_neoplasms_of_liver_and_intrahepatic_bile_ducts_c22,
    CAST("Malignant neoplasm of pancreas (C25)" AS BIGINT) AS malignant_neoplasm_of_pancreas_c25,
    CAST("Malignant neoplasm of larynx (C32)" AS BIGINT) AS malignant_neoplasm_of_larynx_c32,
    CAST("Malignant neoplasms of trachea, bronchus and lung (C33-C34)" AS BIGINT) AS malignant_neoplasms_of_trachea_bronchus_and_lung_c33_c34,
    CAST("Malignant melanoma of skin (C43)" AS BIGINT) AS malignant_melanoma_of_skin_c43,
    CAST("Malignant neoplasm of breast (C50)" AS BIGINT) AS malignant_neoplasm_of_breast_c50,
    CAST("Malignant neoplasm of cervix uteri (C53)" AS BIGINT) AS malignant_neoplasm_of_cervix_uteri_c53,
    CAST("Malignant neoplasms of corpus uteri and uterus, part unspecified (C54-C55)" AS BIGINT) AS malignant_neoplasms_of_corpus_uteri_and_uterus_part_unspecified_c54_c55,
    CAST("Malignant neoplasm of ovary (C56)" AS BIGINT) AS malignant_neoplasm_of_ovary_c56,
    CAST("Malignant neoplasm of prostate (C61)" AS BIGINT) AS malignant_neoplasm_of_prostate_c61,
    CAST("Malignant neoplasms of kidney and renal pelvis (C64-C65)" AS BIGINT) AS malignant_neoplasms_of_kidney_and_renal_pelvis_c64_c65,
    CAST("Malignant neoplasm of bladder (C67)" AS BIGINT) AS malignant_neoplasm_of_bladder_c67,
    CAST("Malignant neoplasms of meninges, brain and other parts of central nervous system (C70-C72)" AS BIGINT) AS malignant_neoplasms_of_meninges_brain_and_other_parts_of_central_nervous_system_c70_c72,
    CAST("Malignant neoplasms of lymphoid, hematopoietic and related tissue (C81-C96)" AS BIGINT) AS malignant_neoplasms_of_lymphoid_hematopoietic_and_related_tissue_c81_c96,
    CAST("All other and unspecified malignant neoplasms (C17,C23-C24,C26-C31,C37-C41,C44-C49,C51-C52,C57-C60,C62-C63,C66,C68-C69,C73-C80,C97)" AS BIGINT) AS all_other_and_unspecified_malignant_neoplasms_c17_c23_c24_c26_c31_c37_c41_c44_c49_c51_c52_c57_c60_c62_c63_c66_c68_c69_c73_c80_c97
FROM "cdc-2na8-fe6s"
