-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_period",
    "locks",
    "direction_of_travel",
    "loading_status",
    "vessel_type",
    "number_of_lockings"
FROM "statistics-austria-ogd-gvd-schleusungen-gvd-schleus-1"
