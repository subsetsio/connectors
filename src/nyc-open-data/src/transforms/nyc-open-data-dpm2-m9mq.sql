-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "docket",
    "address",
    "received_date",
    "borough",
    "block",
    "lot",
    "lmnametype",
    "applicant_name",
    "applicant_co",
    "applicant_address1",
    "applicant_address2",
    "applicant_zip",
    "applicant_city",
    "applicant_state",
    "owner_name",
    "owner_address1",
    "owner_address2",
    "owner_zip",
    "owner_city",
    "owner_state",
    "communityboard",
    "worktypes",
    "regulation_type",
    "issue_date",
    "xcoordinate",
    "ycoordinate",
    "latitude",
    "longitude",
    "regulation_number",
    "owner_co",
    "expiration_date",
    "community_board"
FROM "nyc-open-data-dpm2-m9mq"
