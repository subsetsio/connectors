-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    CAST("time_series" AS BIGINT) AS time_series,
    "hauptaggregate_der_vgr",
    "current_prices_in_million_eur",
    "chained_volume_indices"
FROM "statistics-austria-ogd-vgr104-vgr-konsum-1"
