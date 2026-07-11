-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: WARICC records conflict and cooperation events; event scale and impact are not additive counts.
SELECT
    "case",
    "ccode",
    "cname",
    "date",
    "day",
    "month",
    "year",
    "location",
    "lat_coordin",
    "long_coordin",
    "cyprus",
    "cluster",
    "event",
    "descr",
    "wes",
    "coop",
    "conflict",
    "scale",
    "impact",
    "violence",
    "actor1",
    "actor2",
    "actor3",
    "actor4",
    "actor5",
    "actor6",
    "actor7",
    "actor8",
    "actor9",
    "actor10",
    "direction",
    "international",
    "int_code",
    "neusource",
    "sourceloc",
    "source",
    "med_cover"
FROM "prio-26"
