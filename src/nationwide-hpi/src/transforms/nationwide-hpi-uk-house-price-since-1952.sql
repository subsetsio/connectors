-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The category column includes the published long-run UK series and any companion breakdowns exposed in the source file; compare values within one measure rather than summing categories.
SELECT
    "date",
    "period_label",
    "category",
    "measure",
    "value"
FROM "nationwide-hpi-uk-house-price-since-1952"
