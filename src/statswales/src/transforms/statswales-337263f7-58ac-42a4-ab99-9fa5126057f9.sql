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
FROM "statswales-337263f7-58ac-42a4-ab99-9fa5126057f9"
