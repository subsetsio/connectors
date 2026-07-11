-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Purpose of travel" AS purpose_of_travel,
    "Name of border crossings" AS name_of_border_crossings,
    CAST("Year" AS BIGINT) AS year,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-1800-002v204"
