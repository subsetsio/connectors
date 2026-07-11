-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "hus_year",
    "hus_short_name",
    "indicator",
    "panel_num",
    "panel",
    "unit_num",
    "unit",
    "stub_name_num",
    "stub_name_order",
    "stub_name",
    "stub_label_num",
    "stub_label_order",
    "stub_label",
    "year_num",
    "year",
    "age_num",
    "age",
    "estimate",
    "se",
    "flag",
    "footnote_id_list",
    "footnote_list"
FROM "nchs-aewi-gwni"
