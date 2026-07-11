-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table is stacked by country, technology, source, and year; filter those dimensions before aggregating capacity.
SELECT
    "ID" AS id,
    "technology",
    "source",
    "source_type",
    "weblink",
    "year",
    "type",
    "country",
    "capacity_definition",
    "capacity",
    "comment",
    "energy_source_level_0",
    "energy_source_level_1",
    "energy_source_level_2",
    "energy_source_level_3",
    "technology_level"
FROM "open-power-system-data-national-generation-capacity--national-generation-capacity-stacked"
