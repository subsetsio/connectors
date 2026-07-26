-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Catalog-level dataset may contain mixed measures, geography levels, or reporting periods; inspect column definitions before aggregating.
SELECT
    "package_id",
    "package_title",
    "resource_id",
    "resource_name",
    "resource_format",
    "resource_position",
    "archive_member",
    "row_number",
    "020000100206 02 AK 0200001 Lower Kuskokwim School District 00206 Joann A. Alexie Memorial School 676814 530713 418019 0 92 7357 7357Title I Non Standard 0.97 92 89 Regular school No 1 PK 12" AS 020000100206_02_ak_0200001_lower_kuskokwim_school_district_00206_joann_a_alexie_memorial_school_676814_530713_418019_0_92_7357_7357title_i_non_standard_0_97_92_89_regular_school_no_1_pk_12
FROM "u-s-department-of-education-comparability-of-state-and-local-expenditures-among-schools-within-districts-2011"
