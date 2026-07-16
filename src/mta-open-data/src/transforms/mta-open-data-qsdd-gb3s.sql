-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "agency",
    "asset_category",
    "asset",
    "asset_sub_category_components",
    "total",
    "units",
    "condition_criteria",
    "condition_criteria_percent",
    "count_uc",
    "count_1",
    "count_2",
    "count_3",
    "count_4",
    "count_5",
    "count_other",
    "data_notes"
FROM "mta-open-data-qsdd-gb3s"
