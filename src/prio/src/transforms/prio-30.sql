-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Conflict-onset locations can include imprecise or multiple location fields; use the precision columns when mapping.
SELECT
    "id",
    "location",
    "sidea",
    "sideb",
    "year",
    "onsetprimregion",
    "onsetlocation",
    "locprec",
    "latitude",
    "longitude",
    "sources",
    "coder",
    "startdate",
    "startprec",
    "startdate2",
    "startprec2",
    "epstartdate",
    "epend",
    "ependdate",
    "ependprec",
    "gwnoloc",
    "region",
    "version",
    "int",
    "cumint",
    "type",
    "incomp",
    "terr"
FROM "prio-30"
