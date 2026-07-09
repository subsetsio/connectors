-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix observed historical values with benchmark and extended-benchmark pathway points; filter scenario before interpreting year as observed history or future benchmark.
-- caution: Indicators use different units and normalized scales across sectors, so value and normalized_value should only be compared within a single indicator and unit.
SELECT
    "id",
    "scenario",
    "sector",
    "indicator",
    "country",
    "year",
    "historic_year",
    "variable",
    "value",
    "unit",
    "normalized_value",
    "edition"
FROM "climate-action-tracker-sector-indicators"
