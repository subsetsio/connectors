-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Natural-resource conflict rows are conflict episodes with parties and locations; filter or group by conflict episode before summarising.
SELECT
    "acdid",
    "conflepid",
    "epstartdate",
    "ependdate",
    "begin",
    "end",
    "location",
    "ccode",
    "sidea",
    "sideb",
    "res_confl",
    "aggrav",
    "finance",
    "distribution"
FROM "prio-23"
