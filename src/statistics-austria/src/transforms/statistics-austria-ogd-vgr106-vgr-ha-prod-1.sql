-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_section" AS BIGINT) AS time_section,
    "nace_abteilungen",
    "current_prices_in_million_eur",
    "chained_volume_indices"
FROM "statistics-austria-ogd-vgr106-vgr-ha-prod-1"
