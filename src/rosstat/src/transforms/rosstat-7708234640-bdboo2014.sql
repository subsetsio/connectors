-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row identifier was verified in the raw table; treat rows as source records rather than mergeable observations.
-- caution: Raw data landed as a single source column; use source documentation before interpreting embedded values.
SELECT
    "json"
FROM "rosstat-7708234640-bdboo2014"
