-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "center_name",
    "center_number",
    "report_date",
    "benefits_access_center_wait_time"
FROM "nyc-open-data-fq4m-vjs9"
