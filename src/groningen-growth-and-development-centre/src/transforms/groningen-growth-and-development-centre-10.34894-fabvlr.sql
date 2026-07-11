-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "countrycode",
    "country",
    "currency_unit",
    "year",
    "variable",
    "value"
FROM "groningen-growth-and-development-centre-10.34894-fabvlr"
