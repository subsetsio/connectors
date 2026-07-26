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
    "100654Alabama A & M University 4900 Meridian St Normal AL35762 PO BOX 1357 NORMAL AL35762 010501A 5636001109001002001www.aamu.edu/ 1 1 1 9 1 112 1 93 0 0 0 1 1 2 2161812 1112000000000000 5051011111N-2 R 1R 7.00R 8.00R 15.00R 1.00R 16.00R 32.00R 898772H .R 122000H .R1H .R 45414R 0R 1500R 1000000R 685000R 1000R 200R 0R 55000R 100000H .R 2531043R2R 3550R 0R 375R 25R 15R 4R 452462R 18900R 143297R 7356R 1540R 55R 630R 1107R 1737R 84R 125R 0R 209R 5100R 4900R 125R 1455R 39427R 200R 39627R 75R 10R 85R 39712R 81R 1589R2R1R1R2R1R1R1R2R1R1R1R2R2R2" AS 100654alabama_a_m_university_4900_meridian_st_normal_al35762_po_box_1357_normal_al35762_010501a_5636001109001002001www_aamu_edu_1_1_1_9_1_112_1_93_0_0_0_1_1_2_2161812_1112000000000000_5051011111n_2_r_1r_7_00r_8_00r_15_00r_1_00r_16_00r_32_00r_898772h_r_122000h_r1h_r_45414r_0r_1500r_1000000r_685000r_1000r_200r_0r_55000r_100000h_r_2531043r2r_3550r_0r_375r_25r_15r_4r_452462r_18900r_143297r_7356r_1540r_55r_630r_1107r_1737r_84r_125r_0r_209r_5100r_4900r_125r_1455r_39427r_200r_39627r_75r_10r_85r_39712r_81r_1589r2r1r1r2r1r1r1r2r1r1r1r2r2r2,
    "**************************************************************************;" AS column,
    "**************************************************************************************************." AS column_2
FROM "u-s-department-of-education-academic-libraries-survey-2010-9753e"
