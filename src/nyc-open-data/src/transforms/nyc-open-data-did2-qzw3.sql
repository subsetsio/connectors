-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "ceqr",
    "project_name",
    "block",
    "lot",
    "community_district",
    "house_number",
    "street_name",
    "postcode"
FROM "nyc-open-data-did2-qzw3"
