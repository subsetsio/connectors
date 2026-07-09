-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table stacks separate workbook figures, and each figure is its own slice of the tracker. Rows are only comparable within one figure. Country holds aggregates beside individual partners, and sitc_category holds Total beside commodity breakdowns, so summing over either double counts. Sitc_code is null for figures that report no SITC breakdown, which is why it is not part of the row identity.
SELECT
    "figure",
    "date",
    "direction_of_trade",
    "country",
    "unit",
    "sitc_code",
    "sitc_category",
    "value"
FROM "bruegel-russian-foreign-trade-tracker"
