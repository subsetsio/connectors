-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "adjustment",
    "total_employment_in_1_000_persons",
    "employees_in_1_000_persons",
    "self_employed_in_1_000_persons"
FROM "statistics-austria-ogd-vgr111-vgr-flashes-erwerb-1"
