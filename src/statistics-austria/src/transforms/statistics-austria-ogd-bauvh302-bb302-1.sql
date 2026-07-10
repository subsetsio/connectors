-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "berichtsjahr",
    "commune_partly_abo",
    "building_characteristic",
    "type_of_predominantly_residential_building",
    "number_of_buildings"
FROM "statistics-austria-ogd-bauvh302-bb302-1"
