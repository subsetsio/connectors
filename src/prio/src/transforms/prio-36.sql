-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: GDL SHDI records include multiple administrative levels; filter the level column before aggregating or comparing regions.
SELECT
    "iso_code",
    "country",
    "year",
    "gdlcode",
    "level",
    "region",
    "continent",
    "sgdi",
    "shdi",
    "shdif",
    "shdim",
    "healthindex",
    "healthindexf",
    "healthindexm",
    "incindex",
    "incindexf",
    "incindexm",
    "edindex",
    "edindexf",
    "edindexm",
    "esch",
    "eschf",
    "eschm",
    "msch",
    "mschf",
    "mschm",
    "lifexp",
    "lifexpf",
    "lifexpm",
    "gnic",
    "gnicf",
    "gnicm",
    "lgnic",
    "lgnicf",
    "lgnicm",
    "pop"
FROM "prio-36"
