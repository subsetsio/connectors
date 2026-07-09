-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "dispnum",
    "incidnum",
    "midloc2_location",
    "midloc2_measuringpoint",
    "midloc2_xlongitude",
    "midloc2_ylatitude",
    "midloc2_precision",
    "onset",
    "midloc2_howobtained",
    "midloc2_precision_comment",
    "midloc2_general_comment",
    "priogrid_cell",
    "midloc11_location",
    "midloc11_midlocmeasuringpoint",
    "midloc11_latitude",
    "midloc11_longitude",
    "midloc11_precision"
FROM "correlates-of-war-midloc-incident"
