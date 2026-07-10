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
    "EMILY's List" AS emily_s_list,
    "Justice Dems" AS justice_dems,
    "Indivisible" AS indivisible,
    "PCCC" AS pccc,
    "Our Revolution" AS our_revolution,
    "Sunrise" AS sunrise,
    "Sanders" AS sanders,
    "AOC" AS aoc,
    "Party Committee" AS party_committee
FROM "fivethirtyeight-primary-project-2022-dem-candidates"
