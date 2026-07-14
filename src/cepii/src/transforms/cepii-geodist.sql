-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Distance measures use multiple weighting definitions; choose the distance column appropriate for the gravity specification.
SELECT
    "iso_o",
    "iso_d",
    "contig",
    "comlang_off",
    "comlang_ethno",
    "colony",
    "comcol",
    "curcol",
    "col45",
    "smctry",
    "dist",
    "distcap",
    "distw",
    "distwces"
FROM "cepii-geodist"
