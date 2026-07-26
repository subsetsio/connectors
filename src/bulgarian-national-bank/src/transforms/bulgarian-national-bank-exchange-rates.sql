-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Bulgaria adopted the euro on 2026-01-01 (1 EUR = 1.95583 BGN, the fixed conversion rate): base_currency is 'BGN' before that date and 'EUR' from it, so rate values on either side of the boundary are denominated in different base currencies — split or convert on base_currency before comparing or aggregating across it.
-- caution: rate is base currency per `ratio` units of foreign currency and reverse_rate is foreign currency per 1 unit of base currency in both eras; divide rate by ratio when comparing one-unit exchange rates across currencies (ratio is 100 for some lev-era quotes, 1 in the euro era).
-- caution: Null rate rows before 2026-01-01 are dates with no BNB quote for that currency; the source also no longer serves historical EUR/BGN values, so pre-2026 EUR rows are null (the rate was fixed at 1.95583 BGN per EUR from 1999).
SELECT
    strptime("date", '%Y-%m-%d')::DATE AS date,
    "currency_code",
    "currency_name",
    "base_currency",
    "ratio",
    "rate",
    "reverse_rate",
    "gold"
FROM "bulgarian-national-bank-exchange-rates"
