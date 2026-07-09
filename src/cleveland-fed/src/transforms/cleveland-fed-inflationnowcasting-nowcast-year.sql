-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `label` is the nowcast update stamp for the CURRENT nowcasting cycle only — either a month/day like `08/20` (no year) or a data-release marker like `PCE Jul`. The table is overwritten each cycle and keeps no history; the target month is not encoded in the file.
-- caution: Despite the `year` filename this is the MONTHLY year-over-year nowcast: values are year-over-year percent changes for the current month. The `actual_*` columns carry the realized release value and are populated only on release-marker rows.
-- caution: Series columns that are entirely unpopulated in a cycle are dropped from the file, so the column set varies between runs.
SELECT
    "label",
    "pce_inflation",
    "core_pce_inflation",
    "actual_pce_inflation",
    "actual_core_pce_inflation"
FROM "cleveland-fed-inflationnowcasting-nowcast-year"
