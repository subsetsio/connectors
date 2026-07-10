-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "YEAR" AS year,
    "GoogleKnowlege_Occupation" AS googleknowlege_occupation,
    "Show" AS show,
    "Group" AS group,
    "Raw_Guest_List" AS raw_guest_list
FROM "fivethirtyeight-daily-show-guests-daily-show-guests"
