-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Groups are a taxonomy for browsing series; parent and child groups can overlap, so do not aggregate observations by group without first choosing a non-overlapping category set.
SELECT
    "group_id",
    "name",
    "description",
    "child_group_ids"
FROM "sveriges-riksbank-groups"
