-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The ratio column gives the quoted currency amount; divide rate_bgn by ratio when comparing one-unit exchange rates across currencies.
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "currency_code",
    "currency_name",
    "ratio",
    "rate_bgn",
    "reverse_rate",
    "gold"
FROM "bulgarian-national-bank-exchange-rates"
