-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "artform",
    "ticketssold"
FROM "sg-data-d-3067edabe9ef82011b05fc2bcf99cd8f"
