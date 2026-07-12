-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Notes mix current-statistic comments with jurisdiction metadata, so filter note_type and subject before treating note_text as a comparable field.
SELECT
    "jurisdiction_id",
    "jurisdiction_name",
    "region",
    "note_type",
    "subject",
    "note_text",
    "country_url"
FROM "world-prison-brief-source-notes"
