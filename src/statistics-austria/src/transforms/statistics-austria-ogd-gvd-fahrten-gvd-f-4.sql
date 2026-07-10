-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_period",
    "loading_region",
    "unloading_region",
    "number_of_movements_laden_journeys"
FROM "statistics-austria-ogd-gvd-fahrten-gvd-f-4"
