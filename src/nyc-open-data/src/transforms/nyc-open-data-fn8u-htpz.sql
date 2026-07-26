-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "administrative_district",
    "january_ems_transports",
    "february_ems_transports",
    "march_ems_transports",
    "april_ems_transports",
    "may_ems_transports",
    "june_ems_transports",
    "total_ems_transports",
    "january_ems_transports_emotionalpsychological_condition",
    "february_ems_transports_emotionalpsychological_condition",
    "march_ems_transports_emotionalpsychological_condition",
    "april_ems_transports_emotionalpsychological_condition",
    "may_ems_transports_emotionalpsychological_condition",
    "june_ems_transports_emotionalpsychological_condition",
    "total_transports_emotionalpsychological_conditions"
FROM "nyc-open-data-fn8u-htpz"
