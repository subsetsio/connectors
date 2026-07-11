-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: ACLED records are event-level observations; event types and actors should be filtered before counting conflict incidence.
SELECT
    "conflictid",
    "incompatibility",
    "territory",
    "eventid",
    "eventdate",
    "eventtype",
    "side_a",
    "side_b",
    "countryname",
    "gwno",
    "region",
    "locationname",
    "latitude",
    "longitude",
    "geoprecision",
    "transferactor"
FROM "prio-7"
