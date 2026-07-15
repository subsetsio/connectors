-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "bus_operator",
    "bus_service_no"
FROM "sg-data-d-93a768ea4f271eac5300c38d31be447f"
