-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: These are monthly rates for selected foreign currencies not covered by the ECB daily feed; they should not be mixed with daily ECB reference rates without aligning frequency.
SELECT
    "valid_from",
    "month_number",
    "country",
    "currency_code",
    "currency_name",
    "value"
FROM "national-bank-of-slovakia-exchange-rate-foreign-monthly"
