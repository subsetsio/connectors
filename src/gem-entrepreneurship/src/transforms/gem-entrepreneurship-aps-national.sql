-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: APS rows are national-level survey indicators; compare indicators within the same survey instrument and avoid aggregating different indicator variables as if they were one measure.
-- caution: A small number of source rows have missing economy identifiers, so the raw APS table is published without a strict row key.
SELECT
    "year",
    "economy_code",
    "economy_name",
    "economy_iso",
    "indicator",
    "variable",
    "label",
    "value"
FROM "gem-entrepreneurship-aps-national"
