-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "fiscal_year",
    "households_in_19_unit_buildings",
    "number_of_19_unit_buildings",
    "households_in_10_unit_buildings",
    "number_of_10_unit_buildings",
    "number_of_schools_added",
    "total_number_of_schools_receiving_service"
FROM "nyc-open-data-tiyn-ajjm"
