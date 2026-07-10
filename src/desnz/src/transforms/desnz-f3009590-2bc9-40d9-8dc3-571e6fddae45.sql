-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Sub-regional fuel-poverty statistics mix geography levels, modelled indicators, and periods; filter geography level and measure before aggregation.
SELECT
    "resource",
    "sheet",
    "row_label",
    "series",
    "value_text",
    "value_num"
FROM "desnz-f3009590-2bc9-40d9-8dc3-571e6fddae45"
