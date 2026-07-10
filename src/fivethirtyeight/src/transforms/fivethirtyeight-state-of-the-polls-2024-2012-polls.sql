-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pollster_name",
    "pollster_rating_id",
    "2012_pollster_rating",
    "sponsor_names",
    "sponsor_classifications",
    "partisanship",
    "internal",
    "state",
    "start_date",
    "end_date",
    "tracking",
    "has_prez?" AS has_prez,
    "has_generic?" AS has_generic,
    "has_senate?" AS has_senate,
    "has_house?" AS has_house,
    "media?" AS media,
    "university?" AS university,
    "media_or_university"
FROM "fivethirtyeight-state-of-the-polls-2024-2012-polls"
