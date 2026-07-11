# Data, not logic: the set of currencies the BNR exchange-rate API serves.
# There is no currency-list endpoint, so this is the verified ISO-code set
# discovered by probing https://fxrates.bnr.rw/currency_history/ (each code
# returns a non-empty daily series). XDR is the IMF Special Drawing Right.
# Stable for a central bank; revisit if BNR adds a currency.
CURRENCIES = [
    "USD", "EUR", "GBP", "JPY", "CNY", "CHF", "CAD", "AUD", "ZAR", "KES",
    "UGX", "TZS", "BIF", "INR", "AED", "SAR", "SEK", "NOK", "DKK", "HKD",
    "SGD", "XDR", "ETB", "NGN", "EGP", "GHS", "MAD", "XOF", "XAF", "RUB",
    "BRL", "TRY", "KRW", "PKR", "MUR", "ZMW", "QAR", "KWD", "CZK", "PLN",
    "HUF", "MWK", "SSP",
]

DOCUMENT_ENDPOINTS = [
    "ecostat",
    "mstat",
    "fsstat",
    "fsbs",
    "fsmf",
    "fsins",
    "exstat",
    "pastat",
    "fmdibm",
    "fmdmminst",
    "fmdavg",
    "fmdyc",
]

DOCUMENT_ENTITY_IDS = [
    "balance-of-payment",
    "banking-sector-indicators",
    "central-bank-survey",
    "daily-interbank-market",
    "depository-corporation-survey",
    "insurance-sector-indicators",
    "interbank-market",
    "international-investment-position",
    "internet-banking-statistics",
    "microfinance-indicators",
    "microfinance-sector-indicators",
    "mobile-banking-statistics",
    "mobile-payment-statistics",
    "monthly-average-exchange-rate-for-usd-euro-gbp-dts-yen",
    "monthly-evolution-of-consumer-price-index",
    "monthly-exports",
    "monthly-imports",
    "monthly-producer-price-index",
    "other-depository-corporation-survey",
    "payment-card-based-statistics",
    "repo-market",
    "reverse-repo-market",
    "summary-treasury-bonds",
    "t-bill-market",
]
