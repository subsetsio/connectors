-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "instrnat",
    "institype",
    "indsek",
    "valuta",
    "formål" AS form_l,
    "time",
    "value"
FROM "danmarks-nationalbank-dnrugpi"
