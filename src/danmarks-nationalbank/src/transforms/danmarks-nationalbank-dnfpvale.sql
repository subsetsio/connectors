-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vaerdi1",
    "valuta",
    "time",
    "value"
FROM "danmarks-nationalbank-dnfpvale"
