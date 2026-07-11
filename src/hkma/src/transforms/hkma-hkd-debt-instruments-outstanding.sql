-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    strptime("end_of_month", '%Y-%m')::DATE AS end_of_month,
    "fixed_rate_1y_or_less",
    "fixed_rate_more_than_1y_to_3y",
    "fixed_rate_more_than_3y_to_5y",
    "fixed_rate_more_than_5y",
    "floating_rate_1y_or_less",
    "floating_rate_more_than_1y_to_3y",
    "floating_rate_more_than_3y_to_5y",
    "floating_rate_more_than_5y",
    "osamt_total"
FROM "hkma-hkd-debt-instruments-outstanding"
