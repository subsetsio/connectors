-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency_name",
    "performance_indicator",
    "performance_indicator_description",
    "update_frequency",
    "release_date",
    "july_2015",
    "august_2015",
    "september_2015",
    "october_2015",
    "november_2015",
    "december_2015",
    "january_2016",
    "february_2016",
    "march_2016",
    "april_2016",
    "may_2016"
FROM "nyc-open-data-8r6c-ydwk"
