-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "iyear",
    "Belgium" AS belgium,
    "Denmark" AS denmark,
    "France" AS france,
    "Germany" AS germany,
    "Greece" AS greece,
    "Ireland" AS ireland,
    "Italy" AS italy,
    "Luxembourg" AS luxembourg,
    "Netherlands" AS netherlands,
    "Portugal" AS portugal,
    "Spain" AS spain,
    "United Kingdom" AS united_kingdom
FROM "fivethirtyeight-terrorism-eu-terrorism-fatalities-by-country"
