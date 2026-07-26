-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "admin_district",
    "january_transports",
    "january_emotionalpsych_transports",
    "february_transports",
    "february_emotionalpsych_transports",
    "march_transports",
    "march_emotionalpsych_transports",
    "april_transports",
    "april_emotionalpsych_transports",
    "may_transports",
    "may_emotionalpsych_transports",
    "june_transports",
    "june_emotionalpsych_transports"
FROM "nyc-open-data-89bd-raqa"
