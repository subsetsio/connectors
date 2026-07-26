-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "file",
    "closed",
    "_311" AS 311,
    "sr",
    "steel_curb",
    "sc_cut",
    "ref_to_other",
    "cb",
    "on_street",
    "ifo",
    "cross_st_1",
    "cross_st_2",
    "lin_ft",
    "sq_ft",
    "recd_2",
    "insp",
    "borough"
FROM "nyc-open-data-i2y3-sx2e"
