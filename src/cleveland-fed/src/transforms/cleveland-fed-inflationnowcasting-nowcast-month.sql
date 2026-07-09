-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: `label` is the nowcast update stamp for the CURRENT nowcasting cycle only — either a month/day like `08/20` (no year) or a data-release marker like `PCE Jul`. The table is overwritten each cycle and keeps no history; the target period being nowcast is not encoded in the file.
-- caution: Values are month-over-month percent changes (not annualized). The `actual_*` columns carry the realized release value and are populated only on the release-marker rows; the un-prefixed columns carry the nowcast.
-- caution: Series columns that are entirely unpopulated in a cycle are dropped from the file, so the column set varies between runs.
SELECT
    "label",
    "pce_inflation",
    "core_pce_inflation",
    "actual_pce_inflation",
    "actual_core_pce_inflation"
FROM "cleveland-fed-inflationnowcasting-nowcast-month"
