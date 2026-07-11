-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The source publishes this as an independent aggregate table, but no stable non-null row key was verified in the current raw profile; treat rows as source observations rather than relying on a declared unique key.
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
    "flag"
FROM "nchs-95ax-ymtc"
