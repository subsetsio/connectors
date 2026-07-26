-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "publication_date",
    "nta_code",
    "nta_name",
    "ntaabbrev",
    "baseline",
    "control_scenario_temperature",
    "planned_action_temperature",
    "percent_managed_by_action"
FROM "nyc-open-data-95zn-7w5f"
