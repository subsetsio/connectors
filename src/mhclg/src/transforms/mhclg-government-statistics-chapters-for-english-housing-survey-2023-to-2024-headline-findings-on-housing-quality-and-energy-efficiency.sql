-- mechanical passthrough for accepted-but-empty raw asset `mhclg-government-statistics-chapters-for-english-housing-survey-2023-to-2024-headline-findings-on-housing-quality-and-energy-efficiency`.
-- Kept to preserve full download -> transform graph parity; the spec is waived
-- until supported tabular attachments produce extractable rows.
-- caution: Rows are extracted from heterogeneous publication attachments; the cells column is a JSON array of source row values and may include headings, notes, totals, and mixed table layouts.
SELECT
    "attachment_filename",
    "attachment_title",
    "content_type",
    "sheet_name",
    "row_index",
    "n_cols",
    "cells"
FROM "mhclg-government-statistics-chapters-for-english-housing-survey-2023-to-2024-headline-findings-on-housing-quality-and-energy-efficiency"
