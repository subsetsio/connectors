-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table lists agencies appearing in the Fatal Force source and is not a complete census of law enforcement agencies.
SELECT
    "id",
    "name",
    "type",
    "state",
    "oricodes",
    "total_shootings"
FROM "wapo-fatal-force-fatal-police-shootings-agencies"
