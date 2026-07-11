-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GPIH workbooks are heterogeneous academic spreadsheets; rows can mix sheets, measures, units, places, or aggregation levels from the source workbook. Inspect the table columns before summing or comparing values across rows.
-- caution: No stable row key was verified from the raw workbook profile, so this table is modeled as keyless pass-through data.
SELECT
    "__sheet__" AS sheet,
    "ME" AS me,
    "0.5067342927172568" AS 0_5067342927172568,
    "20881",
    "10254",
    "0.4910684354197596" AS 0_4910684354197596,
    "20326",
    "10381",
    "0.5107251795729607" AS 0_5107251795729607,
    "State" AS state,
    "total",
    "white",
    "White_1" AS white_1,
    "share",
    "totwm",
    "wm/totw" AS wm_totw,
    "wm0-15" AS wm0_15,
    "wm16+" AS wm16,
    "wm16+_2" AS wm16_2,
    "totwf",
    "wf0-15" AS wf0_15,
    "wf16+" AS wf16,
    "wf16+_2" AS wf16_2,
    "over age 16" AS over_age_16,
    "New England" AS new_england,
    "0.49866925568901427" AS 0_49866925568901427,
    "605563",
    "309452",
    "0.511015369168856" AS 0_511015369168856,
    "down",
    "608795",
    "326758",
    "0.5367291124270075" AS 0_5367291124270075,
    "down_2",
    "1214358",
    "2.48" AS 2_48,
    "0.3052971030214749" AS 0_3052971030214749,
    "0.5239064592154867" AS 0_5239064592154867,
    "down_3",
    "0.0151" AS 0_0151
FROM "gpih-age-16-up-shares-1774-1800"
