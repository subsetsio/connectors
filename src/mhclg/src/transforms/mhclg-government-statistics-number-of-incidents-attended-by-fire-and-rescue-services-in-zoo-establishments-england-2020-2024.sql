-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are extracted from heterogeneous publication attachments; the cells column is a JSON array of source row values and may include headings, notes, totals, and mixed table layouts.
SELECT
    "attachment_filename",
    "attachment_title",
    "content_type",
    "sheet_name",
    "row_index",
    "n_cols",
    "cells"
FROM "mhclg-government-statistics-number-of-incidents-attended-by-fire-and-rescue-services-in-zoo-establishments-england-2020-2024"
