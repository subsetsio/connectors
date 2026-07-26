-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "objectid",
    "tasktype",
    "completeddate",
    "workorderglobalid",
    "globalid",
    "crewglobalid",
    "taskentity",
    "staffcpcc",
    "staffcp",
    "staffapsw",
    "labortime",
    "traveltime",
    "staffcpw",
    "staffforester",
    "staffgardener"
FROM "nyc-open-data-45sb-srb5"
