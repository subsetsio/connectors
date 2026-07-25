-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "№ п/п" AS column,
    "Месяц" AS column_2,
    "2017 год (%)" AS 2017,
    "2018 год (%)" AS 2018
FROM "rosstat-7708234640-unemploymentrate2"
