-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This report gives the latest election summary per chamber; use the elections table for historical election events.
SELECT
    "country_name",
    "country_code",
    "structure_of_parliament",
    "struct_parl_status",
    "chamber_name",
    "chamber_code",
    "is_suspended_chamber",
    "designation_mode",
    "election_code",
    "last_election",
    "first_session_date",
    "expect_date_next_election"
FROM "inter-parliamentary-union-report-elections"
