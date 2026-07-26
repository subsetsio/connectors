-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "sch_name",
    "catchment",
    "boro",
    "hsid_no",
    "dbn",
    "remarks",
    "_label" AS label,
    "zoned_dist",
    "boro_text",
    "schooldist",
    "initials",
    "edit_date"
FROM "nyc-open-data-ruu9-egea"
