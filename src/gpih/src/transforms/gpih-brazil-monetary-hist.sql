-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Leticia Arroyo Abad" AS "leticia_arroyo_abad",
    "c1",
    "Silver Conversion resulting from consulted sources" AS "silver_conversion_resulting_from_consulted_sources",
    "c0",
    "1000 rs." AS "1000_rs",
    "500 rs." AS "500_rs",
    "500 rs._2" AS "500_rs_2",
    "500 rs._3" AS "500_rs_3",
    "100 rs." AS "100_rs",
    "50 rs." AS "50_rs",
    "20 rs," AS "20_rs",
    "10 rs." AS "10_rs",
    "10 rs._2" AS "10_rs_2",
    "5 rs." AS "5_rs",
    "3 rs." AS "3_rs",
    "6 Ceitis" AS "6_ceitis",
    "36 reaes e 2 Ceitis" AS "36_reaes_e_2_ceitis",
    "O Reale pesaria" AS "o_reale_pesaria",
    "68.77611940298507" AS "68_77611940298507",
    "graõs" AS "gra_s",
    "0.0499" AS "0_0499",
    "grams de prata /graõ" AS "grams_de_prata_gra",
    "3.431928358208955" AS "3_431928358208955",
    "1 reis" AS "1_reis",
    "3.431928" AS "3_431928",
    "grams"
FROM "gpih-brazil-monetary-hist"
