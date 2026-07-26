-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "the_geom",
    "bin",
    "bbl",
    "borough",
    "block",
    "lot",
    "address",
    "z_grade",
    "z_floor",
    "subgrade",
    "notes1",
    "notes2",
    "notes3",
    "x",
    "y",
    "latitude",
    "longitude",
    "pluto_bbl",
    "council",
    "borocd",
    "ctlabel",
    "boroct2020",
    "nta2020",
    "ntaname",
    "cdta2020",
    "cdtaname"
FROM "nyc-open-data-bsin-59hv"
