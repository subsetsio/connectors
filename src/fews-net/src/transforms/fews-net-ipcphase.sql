-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows include multiple FEWS NET scenarios and projection windows; filter scenario/projection fields before comparing phase values across time.
SELECT
    "source_organization",
    "source_document",
    "datasourcedocument",
    "country",
    "country_code",
    "geographic_group",
    "fewsnet_region",
    "fnid",
    "geographic_unit_name",
    "classification_scale",
    "scenario_name",
    "is_allowing_for_assistance",
    "projection_start",
    "projection_end",
    "value",
    "description",
    "scenario",
    "reporting_date",
    "collection_schedule",
    "collection_status",
    "dataseries_name",
    "geographic_unit_full_name",
    "status",
    "id",
    "data_usage_policy"
FROM "fews-net-ipcphase"
