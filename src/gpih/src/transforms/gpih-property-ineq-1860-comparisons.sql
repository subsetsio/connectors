-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "New England" AS new_england,
    "0.81062582" AS 0_81062582,
    "33.166046" AS 33_166046,
    "56.692307" AS 56_692307,
    "69.331665" AS 69_331665,
    "82.957924" AS 82_957924,
    "16.535767" AS 16_535767,
    "0.50630957" AS 0_50630957,
    "246.21913" AS 246_21913,
    "51.900002" AS 51_900002,
    "17.894042228286803" AS 17_894042228286803,
    "17.91946756602224" AS 17_91946756602224,
    "12.407323282377499" AS 12_407323282377499,
    "Neweng" AS neweng,
    "Midatl" AS midatl,
    "Midatl with DE" AS midatl_with_de,
    "Satl with FL" AS satl_with_fl,
    "Satl no FL" AS satl_no_fl,
    "Satl no FL/DE" AS satl_no_fl_de,
    "ENC" AS enc,
    "WNC" AS wnc,
    "ESC" AS esc,
    "WSC" AS wsc,
    "Mountain" AS mountain,
    "Pacific" AS pacific,
    "All US" AS all_us,
    "Original 13" AS original_13
FROM "gpih-property-ineq-1860-comparisons"
