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
    "100654Alabama A & M University 4900 Meridian Street Normal AL35762 PO BOX 1357 NORMAL AL35762 010501A 5636001109001002001www.aamu.edu/ 1 1 1 9 1 112 1 92 0 0 0 1 2 2 2161812 1112000000000000 4495011111N-2 R 1R 8.00R 11.00R 19.00R 0.00A 9.00A 28.00R 1036237H .R 61000H .R1H .R 77664R 0R 2579R 566314R 142606R 500R 1500R 0R 51608R 115000H .R 1940856R2R 1360R 350R 5R 66R 483665R 19250R 143302R 7522R 373R 230R 603R 47R 9R 0R 56R 6219R 3951R 40R 1300R 30304R 82R 889R1R1R1R2R1R1R1R1R1R1R1" AS 100654alabama_a_m_university_4900_meridian_street_normal_al35762_po_box_1357_normal_al35762_010501a_5636001109001002001www_aamu_edu_1_1_1_9_1_112_1_92_0_0_0_1_2_2_2161812_1112000000000000_4495011111n_2_r_1r_8_00r_11_00r_19_00r_0_00a_9_00a_28_00r_1036237h_r_61000h_r1h_r_77664r_0r_2579r_566314r_142606r_500r_1500r_0r_51608r_115000h_r_1940856r2r_1360r_350r_5r_66r_483665r_19250r_143302r_7522r_373r_230r_603r_47r_9r_0r_56r_6219r_3951r_40r_1300r_30304r_82r_889r1r1r1r2r1r1r1r1r1r1r1,
    "**************************************************************************;" AS column,
    "/****************************************************************************" AS column_2
FROM "u-s-department-of-education-academic-libraries-survey-2012-a396f"
