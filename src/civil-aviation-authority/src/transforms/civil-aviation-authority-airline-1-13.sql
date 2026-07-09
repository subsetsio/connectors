-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "rundate",
    "report_period",
    "aircraft_name",
    "stage_flights",
    "aircraft_hours",
    "release_period",
    "family"
FROM "civil-aviation-authority-airline-1-13"
