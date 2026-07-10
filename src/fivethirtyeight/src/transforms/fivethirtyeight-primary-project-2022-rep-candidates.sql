-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Candidate" AS candidate,
    "Gender" AS gender,
    "Race 1" AS race_1,
    "Race 2" AS race_2,
    "Race 3" AS race_3,
    "Incumbent" AS incumbent,
    "Incumbent Challenger" AS incumbent_challenger,
    "State" AS state,
    "Primary Date" AS primary_date,
    "Office" AS office,
    "District" AS district,
    "Primary Votes" AS primary_votes,
    "Primary %" AS primary,
    "Primary Outcome" AS primary_outcome,
    "Runoff Votes" AS runoff_votes,
    "Runoff %" AS runoff,
    "Runoff Outcome" AS runoff_outcome,
    "2020 Election Stance" AS 2020_election_stance,
    "Trump" AS trump,
    "Trump Date" AS trump_date,
    "Club for Growth" AS club_for_growth,
    "Party Committee" AS party_committee,
    "Renew America" AS renew_america,
    "E-PAC" AS e_pac,
    "VIEW PAC" AS view_pac,
    "Maggie's List" AS maggie_s_list,
    "Winning for Women" AS winning_for_women
FROM "fivethirtyeight-primary-project-2022-rep-candidates"
