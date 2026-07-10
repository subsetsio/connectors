-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Workforce management information mixes payroll, non-payroll, headcount, FTE, and cost summaries; filter resource and sheet before aggregating.
SELECT
    "resource",
    "sheet",
    CAST("row_label" AS BIGINT) AS row_label,
    "series",
    "value_text",
    "value_num"
FROM "desnz-82a5ec99-3790-431b-885c-5a02203cd50f"
