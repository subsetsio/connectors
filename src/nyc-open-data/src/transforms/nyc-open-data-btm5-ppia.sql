-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "segmentid",
    "roadway_name",
    "_from" AS from,
    "_to" AS to,
    "direction",
    "date",
    "_1200100_am" AS 1200100_am,
    "_100200am" AS 100200am,
    "_200300am" AS 200300am,
    "_300400am" AS 300400am,
    "_400500am" AS 400500am,
    "_500600am" AS 500600am,
    "_600700am" AS 600700am,
    "_700800am" AS 700800am,
    "_800900am" AS 800900am,
    "_9001000am" AS 9001000am,
    "_10001100am" AS 10001100am,
    "_11001200pm" AS 11001200pm,
    "_1200100pm" AS 1200100pm,
    "_100200pm" AS 100200pm,
    "_200300pm" AS 200300pm,
    "_300400pm" AS 300400pm,
    "_400500pm" AS 400500pm,
    "_500600pm" AS 500600pm,
    "_600700pm" AS 600700pm,
    "_700800pm" AS 700800pm,
    "_800900pm" AS 800900pm,
    "_9001000pm" AS 9001000pm,
    "_10001100pm" AS 10001100pm,
    "_11001200am" AS 11001200am
FROM "nyc-open-data-btm5-ppia"
