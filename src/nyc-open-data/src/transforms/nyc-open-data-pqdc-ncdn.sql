-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "goal",
    "initiative",
    "report_year",
    "indicator",
    "indicator_value",
    "measurement_type",
    "data_period",
    "_target" AS target
FROM "nyc-open-data-pqdc-ncdn"
