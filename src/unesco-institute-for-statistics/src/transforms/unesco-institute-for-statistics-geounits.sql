-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Mixes countries/territories (type = NATIONAL) with regional aggregates (type = REGIONAL, region_group naming the grouping) in one column — filter on `type` before treating rows as a country list.
SELECT
    "id",
    "name",
    "type",
    "region_group"
FROM "unesco-institute-for-statistics-geounits"
