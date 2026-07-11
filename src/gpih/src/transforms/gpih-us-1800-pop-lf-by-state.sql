-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "state",
    "name",
    "totpop",
    "totpopc",
    "urb800",
    "urb25",
    "wm09",
    "wm1015",
    "wm1625",
    "wm2644",
    "wm45",
    "wf09",
    "wf1015",
    "wf1625",
    "wf2644",
    "wf45",
    "ofptot",
    "stot",
    "totpop2",
    "region1",
    "region2",
    "level",
    "fips",
    "statefip",
    "wmtot",
    "wftot",
    "whtot",
    "nwtot",
    "Connecticut" AS connecticut,
    "1",
    "694",
    "504",
    "88",
    "102",
    "190",
    "72.62247838616715" AS 72_62247838616715
FROM "gpih-us-1800-pop-lf-by-state"
