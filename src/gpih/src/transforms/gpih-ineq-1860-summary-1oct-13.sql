-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS "sheet",
    "Region" AS "region",
    "coeff." AS "coeff",
    "Top !%" AS "top",
    "Top 5%" AS "top_5",
    "Top 10%" AS "top_10",
    "Top 20%" AS "top_20",
    "Next 40%" AS "next_40",
    "Bottom 40%" AS "bottom_40",
    "Mean" AS "mean",
    "Median" AS "median",
    "c10",
    "Neweng" AS "neweng",
    "Midatl" AS "midatl",
    "Midatl with DE" AS "midatl_with_de",
    "Satl with FL" AS "satl_with_fl",
    "Satl no FL" AS "satl_no_fl",
    "Satl no FL/DE" AS "satl_no_fl_de",
    "ENC" AS "enc",
    "WNC" AS "wnc",
    "ESC" AS "esc",
    "WSC" AS "wsc",
    "Mountain" AS "mountain",
    "Pacific" AS "pacific",
    "All US" AS "all_us",
    "Original 13" AS "original_13",
    "Midatl with DE_2" AS "midatl_with_de_2",
    "Satl w/FL" AS "satl_w_fl",
    "Satl no FL_2" AS "satl_no_fl_2",
    "Satl no FL/DE_2" AS "satl_no_fl_de_2",
    "WNC_2" AS "wnc_2",
    "ESC_2" AS "esc_2",
    "WSC_2" AS "wsc_2",
    "All USA" AS "all_usa",
    "Original 13_2" AS "original_13_2"
FROM "gpih-ineq-1860-summary-1oct-13"
