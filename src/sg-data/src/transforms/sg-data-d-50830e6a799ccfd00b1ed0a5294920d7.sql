-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "tariff_category",
    "consumption_block",
    "tariff_before_gst",
    "tariff_after_gst",
    "wbf_before_gst",
    "wbf_after_gst"
FROM "sg-data-d-50830e6a799ccfd00b1ed0a5294920d7"
