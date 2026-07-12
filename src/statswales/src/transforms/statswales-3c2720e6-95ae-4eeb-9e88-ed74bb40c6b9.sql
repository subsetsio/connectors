-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("Data values" AS BIGINT) AS data_values,
    "Data description" AS data_description,
    "Date" AS date,
    "Service" AS service,
    "Local health board or site" AS local_health_board_or_site,
    "Weeks waiting" AS weeks_waiting,
    "Age group" AS age_group,
    "Notes" AS notes
FROM "statswales-3c2720e6-95ae-4eeb-9e88-ed74bb40c6b9"
