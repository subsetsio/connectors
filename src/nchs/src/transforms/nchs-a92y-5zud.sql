-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "topic",
    "subtopic",
    "subtopic_id",
    "taxonomy",
    "taxonomy_id",
    "classification",
    "classification_id",
    "group",
    "group_id",
    "group_order",
    "subgroup",
    "subgroup_id",
    "subgroup_order",
    "nesting_label",
    "nesting_label_id",
    "estimate_type",
    "estimate_type_id",
    "time_period",
    "time_period_id",
    "estimate",
    "standard_error",
    "estimate_lci",
    "estimate_uci",
    "flag",
    "footnote_id_list"
FROM "nchs-a92y-5zud"
