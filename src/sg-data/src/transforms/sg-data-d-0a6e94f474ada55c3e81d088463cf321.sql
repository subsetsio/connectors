-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "energy_consumption_per_dollar_gdp"
FROM "sg-data-d-0a6e94f474ada55c3e81d088463cf321"
