-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Country" AS country,
    "Number of Incidents" AS number_of_incidents,
    "Percent" AS percent,
    "Number Killed" AS number_killed,
    "Number Injured" AS number_injured,
    "Number US Killed" AS number_us_killed,
    "Number US Injured" AS number_us_injured
FROM "fivethirtyeight-terrorism-country-stats-1993-appendix2"
