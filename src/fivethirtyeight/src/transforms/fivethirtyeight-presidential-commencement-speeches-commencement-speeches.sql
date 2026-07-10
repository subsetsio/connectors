-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "president",
    "president_name",
    "title",
    "date",
    "city",
    "state",
    "building",
    "room"
FROM "fivethirtyeight-presidential-commencement-speeches-commencement-speeches"
