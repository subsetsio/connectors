-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("year" AS BIGINT) AS year,
    "region_territorial_structure_of_2024_level_1",
    "occupancy_status_of_the_dwelling_level_1",
    "conventional_dwellings"
FROM "statistics-austria-ogd-rzgwz-gwz-zr-whg-gwz-whg-1"
