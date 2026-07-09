-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: A short window only — the series starts in 2026 and covers a couple of months of NAFEM/NOF trading days, so it is not a historical FX series.
-- caution: `ratedate` is not unique: two dates carry a duplicated row.
-- caution: `dailyVolume` is a traded amount (thousands of US dollars) while `minimumRate`, `maximumRate`, `dailyVariationRange` and `nofr` are naira-per-dollar rates — different units in one row.
SELECT
    "id",
    "ratedate",
    CAST("dailyVolume" AS DOUBLE) AS dailyvolume,
    CAST("minimumRate" AS DOUBLE) AS minimumrate,
    CAST("maximumRate" AS DOUBLE) AS maximumrate,
    CAST("dailyVariationRange" AS DOUBLE) AS dailyvariationrange,
    CAST("nofr" AS DOUBLE) AS nofr
FROM "central-bank-of-nigeria-nafem-nof-rates"
