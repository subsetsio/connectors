-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "school_name",
    "link_to_schools_virtual_opportunities",
    "link_to_schools_myschools_page"
FROM "nyc-open-data-cgkc-y6tk"
