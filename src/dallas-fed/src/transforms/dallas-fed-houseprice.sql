-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include several metrics per country and date; filter metric before comparing country series.
SELECT
    "date",
    "metric",
    "country",
    "value"
FROM "dallas-fed-houseprice"
