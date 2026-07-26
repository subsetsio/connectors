-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "_2014_fy_count" AS 2014_fy_count,
    "_2014_fy_value" AS 2014_fy_value,
    "_2013_fy_count" AS 2013_fy_count,
    "_2013_fy_value" AS 2013_fy_value,
    "_2012_fy_count" AS 2012_fy_count,
    "_2012_fy_value" AS 2012_fy_value,
    "_2011_fy_count" AS 2011_fy_count,
    "_2011_fy_value" AS 2011_fy_value
FROM "nyc-open-data-nd82-bi9f"
