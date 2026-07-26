-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspection_id",
    "omppropid",
    "site_name",
    "boro",
    "district",
    "inspection_date",
    "pip_category",
    "overall_rating",
    "cleanliness_rating"
FROM "nyc-open-data-uwim-9338"
