-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are concatenated from annual and quarterly workbook partitions; filter `frequency` before comparing or aggregating periods.
-- caution: `dimension` carries workbook header sub-dimensions where present, while many indicators have no sub-dimension.
SELECT
    "indicator_en",
    "indicator_ar",
    "dimension",
    "period_label",
    "frequency",
    "year",
    "date",
    "value",
    "source_file"
FROM "cbe-bop--egypts-balance-of-payments"
