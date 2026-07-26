-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "agency",
    "beginning_of_reporting_period",
    strptime("end_of_reporting_period", '%m/%d/%Y')::DATE AS end_of_reporting_period,
    "people_served",
    "applications_distributed",
    "applications_sent_to_boe_by_agency",
    "staff_trained",
    "agency_weblink_to_nyc_votes_yn",
    "web_clicks",
    "rank_choice_voting_materials_distributed"
FROM "nyc-open-data-kkum-y97z"
