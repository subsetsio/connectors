-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Candidate" AS candidate,
    "State" AS state,
    "District" AS district,
    "Office Type" AS office_type,
    "Race Type" AS race_type,
    "Race Primary Election Date" AS race_primary_election_date,
    "Primary Status" AS primary_status,
    "Primary Runoff Status" AS primary_runoff_status,
    "General Status" AS general_status,
    "Primary %" AS primary,
    "Won Primary" AS won_primary,
    "Rep Party Support?" AS rep_party_support,
    "Trump Endorsed?" AS trump_endorsed,
    "Bannon Endorsed?" AS bannon_endorsed,
    "Great America Endorsed?" AS great_america_endorsed,
    "NRA Endorsed?" AS nra_endorsed,
    "Right to Life Endorsed?" AS right_to_life_endorsed,
    "Susan B. Anthony Endorsed?" AS susan_b_anthony_endorsed,
    "Club for Growth Endorsed?" AS club_for_growth_endorsed,
    "Koch Support?" AS koch_support,
    "House Freedom Support?" AS house_freedom_support,
    "Tea Party Endorsed?" AS tea_party_endorsed,
    "Main Street Endorsed?" AS main_street_endorsed,
    "Chamber Endorsed?" AS chamber_endorsed,
    "No Labels Support?" AS no_labels_support
FROM "fivethirtyeight-primary-candidates-2018-rep-candidates"
