-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "dbn",
    "districtwide",
    "school_name",
    "prioritized_group",
    "diversitytarget",
    "total_offers_to_school",
    "offers_to_prioritized_group",
    "diversity_percentage_from_offers",
    "met_diversity_goal"
FROM "nyc-open-data-nzf8-y8wb"
