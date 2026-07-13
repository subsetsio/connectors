-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "investland",
    "invsektor",
    "investfond",
    "hovedkat",
    "misbrug2",
    "forvalt",
    "risiko",
    "data",
    "time",
    "value"
FROM "danmarks-nationalbank-dnifhvem"
