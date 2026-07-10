-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "jahr",
    "commune_partly_abo",
    "type_of_construction_measure",
    "new_construction_of_entire_buildings_type_of_predominant_residential_building",
    "number_of_dwellings"
FROM "statistics-austria-ogd-bewwohn303-bb303-1"
