-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Start" AS start,
    "End" AS end,
    "Pollster" AS pollster,
    "Sponsor" AS sponsor,
    "SampleSize" AS samplesize,
    "Pop" AS pop,
    "tracking",
    "Text" AS text,
    "Category" AS category,
    "Include?" AS include,
    "Yes" AS yes,
    "No" AS no,
    "Unsure" AS unsure,
    "Rep Sample" AS rep_sample,
    "Rep Yes" AS rep_yes,
    "Rep No" AS rep_no,
    "Dem Sample" AS dem_sample,
    "Dem Yes" AS dem_yes,
    "Dem No" AS dem_no,
    "Ind Sample" AS ind_sample,
    "Ind Yes" AS ind_yes,
    "Ind No" AS ind_no,
    "URL" AS url,
    "Notes" AS notes
FROM "fivethirtyeight-impeachment-polls-impeachment-polls"
