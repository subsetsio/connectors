-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "vision",
    "goal",
    "indicator",
    "report_year",
    "indicator_value",
    "measurement_type",
    "target_value",
    "target_year"
FROM "nyc-open-data-f34v-uffx"
