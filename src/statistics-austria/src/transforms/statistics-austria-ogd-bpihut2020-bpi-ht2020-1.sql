-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "building_construction_and_civil_engineering",
    "building_construction",
    "civil_engineering",
    "construction_of_residential_buildings",
    "other_building_construction",
    "road_construction",
    "bridge_construction",
    "other_civil_engineering"
FROM "statistics-austria-ogd-bpihut2020-bpi-ht2020-1"
