-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: LAGOS lake ids and NHD ids both appear; this table's verified row identity is the NHD id.
SELECT
    "lagoslakeid",
    "nhdid",
    "nhd_lat",
    "nhd_long",
    "lagosname1",
    "meandepth",
    "meandepthsource",
    "maxdepth",
    "maxdepthsource",
    "legacyid"
FROM "lagos-ne-lake-identifiers-and-morphometry"
