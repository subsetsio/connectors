-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "provision_of_help_utilisation_of_health_care",
    "group_of_persons",
    CAST("year" AS BIGINT) AS year,
    "value"
FROM "statistics-estonia-sh31.px"
