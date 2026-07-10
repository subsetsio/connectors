-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "source_file",
    "row_number",
    "time_section",
    "group_of_construction_cost_index_total_contractors",
    "total",
    "wages",
    "other"
FROM "statistics-austria-ogd-bkiwhsiedlg2025-bki-ws25-1"
