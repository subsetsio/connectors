-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "bitumen_total",
    "bitumen_domestic",
    "bitumen_non_domestic",
    "bitumen_germany",
    "bitumen_italy",
    "bitumen_other_countries"
FROM "statistics-austria-ogd-bkistrassebitumen2025-bki-sb25-1"
