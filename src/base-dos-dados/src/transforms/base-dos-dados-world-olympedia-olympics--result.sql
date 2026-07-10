-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "result_id",
    "event_title",
    "edition",
    "edition_id",
    "sport",
    "result_date",
    "result_location",
    "result_participants",
    "result_format",
    "result_detail",
    "result_description"
FROM "base-dos-dados-world-olympedia-olympics--result"
