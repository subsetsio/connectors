-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are not uniquely keyed by the exposed PxWeb label dimensions in the raw download; duplicate label-level combinations exist, so no table-level grain is asserted.
SELECT
    "time_of_construction",
    "type_of_building_and_number_of_dwellings",
    "location",
    "value"
FROM "statistics-estonia-rl707.px"
