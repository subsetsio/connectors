-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "event_id",
    "title",
    "date",
    "start_time",
    "end_time",
    "location_description",
    "description",
    "snippet",
    "phone",
    "email",
    "cost_free",
    "cost_description",
    "must_see",
    "url",
    "notice"
FROM "nyc-open-data-fudw-fgrp"
