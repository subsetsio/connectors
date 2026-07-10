-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Date" AS date,
    "title:""Puerto Rico""" AS title_puerto_rico,
    "title:""Puerto Rico"" AND (title:Trump OR title:President)" AS title_puerto_rico_and_title_trump_or_title_president,
    "title:Florida" AS title_florida,
    "title:Florida AND (title:Trump OR title:President)" AS title_florida_and_title_trump_or_title_president,
    "title:Texas" AS title_texas,
    "title:Texas AND (title:Trump OR title:President)" AS title_texas_and_title_trump_or_title_president
FROM "fivethirtyeight-puerto-rico-media-mediacloud-trump"
