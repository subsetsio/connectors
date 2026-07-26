-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "record_id",
    "date_and_time",
    "notificationtype",
    "notification_title",
    "email_body"
FROM "nyc-open-data-8vv7-7wx3"
