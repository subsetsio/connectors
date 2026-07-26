-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "isp_name_dba_name",
    "technology_type",
    "number_of_census_blocks_served"
FROM "nyc-open-data-7vk6-9w2d"
