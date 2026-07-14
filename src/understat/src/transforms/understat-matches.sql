-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "isResult" AS isresult,
    "h",
    "a",
    "goals",
    "xG" AS xg,
    "datetime",
    "forecast",
    "league",
    "season"
FROM "understat-matches"
