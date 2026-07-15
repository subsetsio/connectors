-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Temporal series table; confirm aggregation dimensions before summing across categories.
SELECT
    "nea_reg_no_sinnea",
    "company",
    "trade_brand_name",
    "active_ingredient",
    "percentage_ww",
    "forumulation",
    "reg_date",
    "classification"
FROM "sg-data-d-9e879860c62144c6f44011ad4bb04b82"
