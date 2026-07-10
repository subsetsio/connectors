-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "C0" AS c0,
    "Pct. Of major sports searches" AS pct_of_major_sports_searches,
    "_1" AS 1,
    "_2" AS 2,
    "_3" AS 3,
    "_4" AS 4,
    "_5" AS 5,
    "_6" AS 6,
    "_7" AS 7
FROM "fivethirtyeight-nfl-fandom-nfl-fandom-data-google-trends"
