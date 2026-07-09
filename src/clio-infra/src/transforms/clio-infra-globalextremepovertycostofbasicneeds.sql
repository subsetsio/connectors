-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Each table is one Clio Infra indicator; the meaning and units of value are specific to that indicator and should not be combined across indicators without consulting the source metadata.
SELECT
    "ccode",
    "country",
    "year",
    "value"
FROM "clio-infra-globalextremepovertycostofbasicneeds"
