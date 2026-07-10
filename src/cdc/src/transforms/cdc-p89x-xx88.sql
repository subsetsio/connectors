-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Round" AS BIGINT) AS round,
    "Topic" AS topic,
    "Indicator" AS indicator,
    "Title" AS title,
    "Demographic Variable" AS demographic_variable,
    "Demographic Variable Label" AS demographic_variable_label,
    "Percent Estimate" AS percent_estimate,
    "Confidence Interval" AS confidence_interval
FROM "cdc-p89x-xx88"
