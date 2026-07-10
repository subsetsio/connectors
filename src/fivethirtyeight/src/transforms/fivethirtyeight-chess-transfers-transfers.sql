-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "url",
    "ID" AS id,
    "Federation" AS federation,
    "Form.Fed" AS form_fed,
    "Transfer Date" AS transfer_date
FROM "fivethirtyeight-chess-transfers-transfers"
