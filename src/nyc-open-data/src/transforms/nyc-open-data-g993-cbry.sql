-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "school_name",
    "_1213_initative" AS 1213_initative,
    "location_category_description",
    "borough"
FROM "nyc-open-data-g993-cbry"
