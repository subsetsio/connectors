-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `dimension` can distinguish debtor-sector columns from the workbook header; include it when grouping indicators.
-- caution: Rows combine annual and quarterly observations; use `frequency` to avoid mixing time granularities.
-- caution: The source workbook can repeat observations without a stable non-null row identifier; treat rows as source observations rather than keyed facts.
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
FROM "cbe-external-debt--external-debt-by-debtor"
