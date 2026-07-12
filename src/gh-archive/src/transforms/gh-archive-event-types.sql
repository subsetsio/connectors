-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Reference taxonomy is curated from GitHub's public event-type documentation and may lag newly introduced or retired event classes until the connector is updated.
SELECT
    "event_type",
    "description",
    "docs_url"
FROM "gh-archive-event-types"
