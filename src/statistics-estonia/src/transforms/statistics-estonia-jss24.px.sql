-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("reference_period" AS BIGINT) AS reference_period,
    "experience_of_intimate_partner_or_non_partner_violence_stalking_or_sexual_harassment_at_work",
    "indicator",
    "value"
FROM "statistics-estonia-jss24.px"
