-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "School_name" AS school_name,
    "school_section",
    "cca_grouping_desc",
    "cca_generic_name",
    "cca_customized_name"
FROM "sg-data-d-9aba12b5527843afb0b2e8e4ed6ac6bd"
