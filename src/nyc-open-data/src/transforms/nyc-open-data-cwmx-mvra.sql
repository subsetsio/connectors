-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "extract_date",
    "specimen_date",
    "number_tested",
    "number_confirmed",
    "number_hospitalized",
    "number_deaths"
FROM "nyc-open-data-cwmx-mvra"
