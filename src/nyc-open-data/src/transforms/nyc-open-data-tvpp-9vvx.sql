-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_id",
    "event_name",
    "start_datetime",
    "end_datetime",
    "event_agency",
    "event_type",
    "event_borough",
    "event_location",
    "event_street_side",
    "street_closure_type",
    "community_board",
    "police_precinct",
    "cemsid"
FROM "nyc-open-data-tvpp-9vvx"
