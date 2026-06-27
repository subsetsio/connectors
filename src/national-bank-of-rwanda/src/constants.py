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
