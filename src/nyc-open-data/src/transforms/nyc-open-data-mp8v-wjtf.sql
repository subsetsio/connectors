-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "inspectionid",
    "prnumber",
    "pr_overall_condition",
    "pr_litter",
    "pr_graffiti",
    "pr_amenities",
    "pr_structural"
FROM "nyc-open-data-mp8v-wjtf"
