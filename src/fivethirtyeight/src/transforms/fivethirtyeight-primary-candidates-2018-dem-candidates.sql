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
    "Partisan Lean" AS partisan_lean,
    "Primary %" AS primary,
    "Won Primary" AS won_primary,
    "Race" AS race,
    "Veteran?" AS veteran,
    "LGBTQ?" AS lgbtq,
    "Elected Official?" AS elected_official,
    "Self-Funder?" AS self_funder,
    "STEM?" AS stem,
    "Obama Alum?" AS obama_alum,
    "Party Support?" AS party_support,
    "Emily Endorsed?" AS emily_endorsed,
    "Guns Sense Candidate?" AS guns_sense_candidate,
    "Biden Endorsed?" AS biden_endorsed,
    "Warren Endorsed? " AS warren_endorsed,
    "Sanders Endorsed?" AS sanders_endorsed,
    "Our Revolution Endorsed?" AS our_revolution_endorsed,
    "Justice Dems Endorsed?" AS justice_dems_endorsed,
    "PCCC Endorsed?" AS pccc_endorsed,
    "Indivisible Endorsed?" AS indivisible_endorsed,
    "WFP Endorsed?" AS wfp_endorsed,
    "VoteVets Endorsed?" AS votevets_endorsed,
    "No Labels Support?" AS no_labels_support
FROM "fivethirtyeight-primary-candidates-2018-dem-candidates"
