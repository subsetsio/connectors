-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "indicator",
    "panel",
    "panel_num",
    "unit",
    "unit_num",
    "stub_name",
    "stub_name_num",
    "stub_label",
    "stub_label_num",
    "year",
    "year_num",
    "age",
    "age_num",
    "estimate",
    "se",
    "flag"
FROM "nchs-2m93-xvra"
