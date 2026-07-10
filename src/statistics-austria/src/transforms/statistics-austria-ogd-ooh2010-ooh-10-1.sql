-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_series",
    "owner_occupied_housing_price_index",
    "aquisition_of_dwellings",
    "new_dwellings",
    "purchase_of_new_dwellings",
    "self_build_dwellings_and_major_repairs",
    "existing_dwellings_new_to_households",
    "other_costs_related_to_the_purchase_of_the_dwelling",
    "ownership_of_dwellings",
    "major_repairs_and_maintenance",
    "insurances_connected_with_dwelling"
FROM "statistics-austria-ogd-ooh2010-ooh-10-1"
