-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Metric codes in the catalog can repeat across category, subcategory, unit, and type, so use the full catalog grain when treating rows as definitions.
SELECT
    "metric",
    "full_name",
    "description",
    "product",
    "category",
    "subcategory",
    "unit",
    "data_type",
    "type",
    "display_name",
    "docs_url"
FROM "coin-metrics-asset-metrics-catalog"
