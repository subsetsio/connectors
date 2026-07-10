-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "Harvey" AS harvey,
    "Irma" AS irma,
    "Maria" AS maria,
    "Jose" AS jose
FROM "fivethirtyeight-puerto-rico-media-tv-hurricanes"
