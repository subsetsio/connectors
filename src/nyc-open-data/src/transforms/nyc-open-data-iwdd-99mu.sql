-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "estimated_bid_date",
    "agency",
    "agency_unit",
    "trades",
    "project_description",
    "award_method",
    "project_id",
    "epin",
    "engineers_estimate_amount_in_000s",
    "status_of_bid",
    "borough_of_work_bronx",
    "borough_of_work_brooklyn",
    "borough_of_work_manhattan",
    "borough_of_work_queens",
    "borough_of_work_staten_island",
    "borough_of_work_upstate",
    "prebid_meeting_yn",
    "subject_to_ll1_yn",
    "federal_or_state_goals",
    "is_apprenticeship_required_yn",
    "subject_to_a_pla_yn",
    "subject_to_damages_for_delay",
    "onenyc_yn"
FROM "nyc-open-data-iwdd-99mu"
