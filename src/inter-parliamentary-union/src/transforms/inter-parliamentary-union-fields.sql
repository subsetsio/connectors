-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "field_id",
    "entity_type",
    "data_type",
    "field_name",
    "description",
    "short_description",
    "label",
    "timeseries_update_frequency",
    "timeseries_type",
    "is_comparable",
    "is_explorable",
    "is_parliament_page",
    "data_entry_format",
    "is_timeseries",
    "is_searchable",
    "timeseries_from_date",
    "cardinality",
    "is_private",
    "is_mandatory",
    "timeseries_validity",
    "is_bicameral_only",
    "taxonomy_key",
    "is_multiple",
    "is_translated",
    "is_computed",
    "unit",
    "max_length",
    "decimals_precision"
FROM "inter-parliamentary-union-fields"
