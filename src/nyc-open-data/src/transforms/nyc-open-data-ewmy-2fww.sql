-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "budget_size",
    "_2014_fycount" AS 2014_fycount,
    "_2014_fyvalue" AS 2014_fyvalue,
    "_2013_fycount" AS 2013_fycount,
    "_2013_fy_value" AS 2013_fy_value,
    "_2012_fycount" AS 2012_fycount,
    "_2012_fy_value" AS 2012_fy_value,
    "_2011_fycount" AS 2011_fycount,
    "_2011_fy_value" AS 2011_fy_value
FROM "nyc-open-data-ewmy-2fww"
