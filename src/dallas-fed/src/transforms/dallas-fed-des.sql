-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include different respondent segments and basis values; filter segment and basis before comparing series.
SELECT
    "date",
    "segment",
    "basis",
    "series_code",
    "component",
    "value"
FROM "dallas-fed-des"
