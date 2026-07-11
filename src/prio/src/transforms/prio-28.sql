-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Institutional-variance measures are country-year indicators; democracy-related columns are alternative measures, not mutually exclusive rows.
SELECT
    "year",
    "ssno",
    "name",
    "sysmember",
    "parlpres",
    "federal",
    "indexksg",
    "election_dem",
    "election",
    "continent",
    "region",
    "parlpres_dem",
    "federal_dem",
    "gwno",
    "primkey"
FROM "prio-28"
