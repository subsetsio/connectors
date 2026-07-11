-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "group_name",
    "group_label",
    "group_description",
    "group_parent",
    "group_type",
    "group_sort_order",
    "group_fields"
FROM "inter-parliamentary-union-groups"
