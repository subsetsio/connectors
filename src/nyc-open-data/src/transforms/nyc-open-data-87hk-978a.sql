-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "administrative_district",
    "january_ems_transports_for_emotionalpsychological_conditions",
    "january_ems_transports",
    "february_ems_transports_for_emotionalpsychological_conditions",
    "february_ems_transports",
    "march_ems_transports_for_emotionalpsychological_conditions",
    "march_ems_transports",
    "april_ems_transports_for_emotionalpsychological_conditions",
    "april_ems_transports",
    "may_ems_transports_for_emotionalpsychological_conditions",
    "may_ems_transports",
    "june_ems_transports_for_emotionalpsychological_conditions",
    "june_ems_transports",
    "total_ems_transports_for_emotionalpsychological_conditions",
    "total_ems_transports"
FROM "nyc-open-data-87hk-978a"
