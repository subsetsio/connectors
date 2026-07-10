-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "Texas" AS texas,
    """Puerto Rico""" AS puerto_rico,
    "Florida" AS florida
FROM "fivethirtyeight-puerto-rico-media-mediacloud-states"
