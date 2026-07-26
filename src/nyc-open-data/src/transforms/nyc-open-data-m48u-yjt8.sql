-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_id",
    "committee",
    "meeting_date",
    "meeting_time",
    "meeting_location",
    "note",
    "agenda_status",
    "minutes_status",
    "modified_date",
    "url"
FROM "nyc-open-data-m48u-yjt8"
