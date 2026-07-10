-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "region_territorial_structure_of_2024_level_1",
    "type_of_building_predominant_use_level_1",
    "buildings"
FROM "statistics-austria-ogd-rzgwz-gwz-zr-geb-gwz-geb-1"
