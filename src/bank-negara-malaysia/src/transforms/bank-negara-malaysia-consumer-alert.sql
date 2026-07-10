-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The alert list is a current reference list, not a complete time series of all historical alert states.
SELECT
    "name",
    "regisration_number",
    "added_date",
    "websites"
FROM "bank-negara-malaysia-consumer-alert"
